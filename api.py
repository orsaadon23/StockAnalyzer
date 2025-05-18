from flask import Flask, jsonify
import mysql.connector
import os
import numpy as np
from datetime import datetime, timedelta

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'stockuser'),
        password=os.getenv('DB_PASSWORD', 'stockpassword'),
        database=os.getenv('DB_NAME', 'data')
    )

@app.route('/stock/<symbol>', methods=['GET'])
def get_stock(symbol):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get the latest stock price for the given symbol
        query = """
            SELECT symbol, price, timestamp
            FROM stock
            WHERE symbol = %s
            ORDER BY timestamp DESC
            LIMIT 1
        """
        cursor.execute(query, (symbol,))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result:
            return jsonify({
                'symbol': result['symbol'],
                'price': result['price'],
                'timestamp': result['timestamp'].isoformat()
            })
        else:
            return jsonify({'error': f'No data found for symbol {symbol}'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cup-and-handle/<symbol>', methods=['GET'])
def check_cup_and_handle(symbol):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get stock data from the last 3 days
        three_days_ago = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S')
        query = """
            SELECT symbol, price, timestamp
            FROM stock
            WHERE symbol = %s AND timestamp >= %s
            ORDER BY timestamp DESC
        """
        cursor.execute(query, (symbol, three_days_ago))
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        if not results:
            return jsonify({'error': f'No data found for symbol {symbol}'}), 404
        
        # Reverse to get chronological order
        results.reverse()
        
        # Extract prices and timestamps
        prices = [float(record['price']) for record in results]
        timestamps = [record['timestamp'] for record in results]
        
        # Check for cup and handle pattern
        has_pattern, details = detect_cup_and_handle(prices, timestamps)
        
        return jsonify({
            'symbol': symbol,
            'has_cup_and_handle_pattern': has_pattern,
            'details': details
        })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def detect_cup_and_handle(prices, timestamps):
    """
    Detect cup and handle pattern in price data.
    
    The pattern consists of:
    1. A downward price movement
    2. A rounded bottom (cup)
    3. A slight downward drift (handle)
    4. A breakout upward
    
    Returns:
    - Boolean indicating if the pattern is detected
    - Dictionary with details about the pattern
    """
    if len(prices) < 30:
        return False, {"error": "Not enough data points to detect pattern"}
    
    try:
        # Convert to numpy array for easier manipulation
        prices_array = np.array(prices)
        
        # Smooth the data to reduce noise
        window_size = min(5, len(prices) // 10)
        smoothed = np.convolve(prices_array, np.ones(window_size)/window_size, mode='valid')
        
        # Find local minima and maxima
        window = min(7, len(smoothed) // 5)
        
        # Parameters for cup detection
        cup_depth_threshold = 0.03  # Minimum 3% drop for cup 
        handle_depth_threshold = 0.015  # Minimum 1.5% drop for handle
        handle_size_threshold = min(len(smoothed) // 5, 10)  # Handle should be smaller than cup
        
        # Find potential cup bottom
        cup_bottom_idx = None
        cup_start_idx = None
        cup_end_idx = None
        
        # Look for a price drop followed by a recovery (cup shape)
        for i in range(window, len(smoothed) - window):
            # Check if this point is a local minimum
            if all(smoothed[i] <= smoothed[i-j] for j in range(1, window+1)) and \
               all(smoothed[i] <= smoothed[i+j] for j in range(1, window+1)):
                
                # Find start of cup (local maximum before the minimum)
                start_idx = max(0, i - window * 2)
                for j in range(i-1, start_idx, -1):
                    if all(smoothed[j] >= smoothed[j-k] for k in range(1, min(j, window)+1)):
                        cup_start_idx = j
                        break
                
                # Find end of cup (local maximum after the minimum)
                end_idx = min(len(smoothed) - 1, i + window * 2)
                for j in range(i+1, end_idx):
                    if all(smoothed[j] >= smoothed[j+k] for k in range(1, min(len(smoothed)-j-1, window)+1)):
                        cup_end_idx = j
                        break
                
                if cup_start_idx is not None and cup_end_idx is not None:
                    # Verify cup depth
                    cup_depth = (smoothed[cup_start_idx] - smoothed[i]) / smoothed[cup_start_idx]
                    if cup_depth >= cup_depth_threshold:
                        cup_bottom_idx = i
                        break
        
        if cup_bottom_idx is None or cup_start_idx is None or cup_end_idx is None:
            return False, {"reason": "No cup formation detected"}
        
        # Check for handle formation after the cup
        handle_start_idx = cup_end_idx
        handle_bottom_idx = None
        handle_end_idx = None
        
        # Handle should be within a reasonable distance after the cup
        max_handle_distance = min(len(smoothed) - handle_start_idx - 1, handle_size_threshold * 2)
        
        for i in range(handle_start_idx + 1, min(len(smoothed), handle_start_idx + max_handle_distance)):
            # Check if this point is a local minimum
            if i > handle_start_idx + 1 and i < len(smoothed) - 1 and \
               smoothed[i] < smoothed[i-1] and smoothed[i] < smoothed[i+1]:
                handle_bottom_idx = i
                
                # Find end of handle (local maximum or end of data)
                for j in range(i+1, min(len(smoothed), i + handle_size_threshold)):
                    if j == len(smoothed) - 1 or (smoothed[j] > smoothed[j-1] and smoothed[j] > smoothed[j+1]):
                        handle_end_idx = j
                        break
                
                if handle_end_idx is not None:
                    # Verify handle depth and size
                    handle_depth = (smoothed[handle_start_idx] - smoothed[handle_bottom_idx]) / smoothed[handle_start_idx]
                    handle_size = handle_end_idx - handle_start_idx
                    
                    if handle_depth >= handle_depth_threshold and handle_size <= handle_size_threshold:
                        # Check if there's an upward breakout after the handle
                        if handle_end_idx < len(smoothed) - 1 and smoothed[-1] > smoothed[handle_end_idx]:
                            return True, {
                                "cup_start": timestamps[cup_start_idx].isoformat() if cup_start_idx < len(timestamps) else None,
                                "cup_bottom": timestamps[cup_bottom_idx].isoformat() if cup_bottom_idx < len(timestamps) else None,
                                "cup_end": timestamps[cup_end_idx].isoformat() if cup_end_idx < len(timestamps) else None,
                                "handle_start": timestamps[handle_start_idx].isoformat() if handle_start_idx < len(timestamps) else None,
                                "handle_bottom": timestamps[handle_bottom_idx].isoformat() if handle_bottom_idx < len(timestamps) else None,
                                "handle_end": timestamps[handle_end_idx].isoformat() if handle_end_idx < len(timestamps) else None,
                                "cup_depth_percentage": round(cup_depth * 100, 2),
                                "handle_depth_percentage": round(handle_depth * 100, 2)
                            }
        
        return False, {"reason": "Cup formation found but no valid handle or breakout detected"}
        
    except Exception as e:
        return False, {"error": str(e)}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 