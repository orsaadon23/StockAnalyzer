import argparse
import requests
import mysql.connector
import os
import datetime
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'mysql'),
        user=os.getenv('DB_USER', 'stockuser'),
        password=os.getenv('DB_PASSWORD', 'stockpassword'),
        database=os.getenv('DB_NAME', 'data')
    )

def fetch_stock_price(symbol):
    # Using Alpha Vantage API (free tier)
    # You'll need to register for a free API key at https://www.alphavantage.co/
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY', 'demo')
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}'
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if "Global Quote" in data and data["Global Quote"]:
            quote = data["Global Quote"]
            if "05. price" in quote and quote["05. price"]:
                return float(quote["05. price"])
        
        print(f"Error fetching data for {symbol}: {data}")
        return None
    except Exception as e:
        print(f"Exception while fetching stock price: {e}")
        return None

def store_stock_price(symbol, price):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        query = """
            INSERT INTO stock (timestamp, symbol, price)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (timestamp, symbol, price))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"Successfully stored price for {symbol}: ${price} at {timestamp}")
        return True
    except Exception as e:
        print(f"Error storing data: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Fetch and store current stock price')
    parser.add_argument('symbol', help='Stock symbol to fetch (e.g., AAPL)')
    
    args = parser.parse_args()
    symbol = args.symbol.upper()
    
    print(f"Fetching current price for {symbol}...")
    price = fetch_stock_price(symbol)
    
    if price:
        print(f"Current price for {symbol}: ${price}")
        if store_stock_price(symbol, price):
            print("Data successfully stored in database")
        else:
            print("Failed to store data in database")
            sys.exit(1)
    else:
        print(f"Failed to fetch price for {symbol}")
        sys.exit(1)

if __name__ == "__main__":
    main() 