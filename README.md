# StockAnalyzer

A system to collect and serve stock price data for major tech companies with pattern detection capabilities.

## Components

1. MySQL database - Stores stock price data with timestamp, symbol, and price
2. Flask API - Provides endpoints to retrieve the latest stock price and detect patterns
3. Collector Service - A single service that collects price data for multiple stocks on different schedules:
   - Apple (AAPL)
   - Microsoft (MSFT)
   - Alphabet/Google (GOOGL)
   - Amazon (AMZN)
   - Nvidia (NVDA)
   - Meta (META)
   - Tesla (TSLA)

## Installation

### Prerequisites
- Docker and Docker Compose
- Python 3.9+
- An Alpha Vantage API key

### Install Dependencies
If running components outside of Docker:
```
pip install -r requirements.txt
```

### Environment Setup
1. **IMPORTANT**: Get your free Alpha Vantage API key:
   - Go to https://www.alphavantage.co/support/#api-key
   - Register for a free API key (takes less than 20 seconds)
   - Create a .env file in the project root and set your API key:
   
   ```
   ALPHA_VANTAGE_API_KEY=your_api_key
   DB_USER=stockuser
   DB_PASSWORD=stockpassword
   ```
   
   **Note**: Without setting a valid API key, most requests will fail with a demo key limitation error.

## Deployment

Start all services using Docker Compose:
```
docker-compose up -d
```

This will:
1. Create a MySQL database
2. Start the Flask API server
3. Launch the collector service that gathers stock data every 5 minutes

## Usage

### Retrieve the latest stock price for a company
```
curl http://localhost:5000/stock/AAPL  
# Replace AAPL with any supported symbol (AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA)
```

### Check for Cup and Handle Pattern
```
curl http://localhost:5000/cup-and-handle/AAPL  
# Replace AAPL with any supported symbol
```

## Cup and Handle Pattern Detection

The cup-and-handle pattern is a bullish continuation pattern where the price action resembles a cup (a "U" shape) followed by a handle (a slight downward drift). The system detects this pattern by:

1. Analyzing historical price data for a specific stock
2. Identifying a U-shaped price trajectory (the cup)
3. Detecting a small downward/sideways consolidation period following the cup (the handle)
4. Calculating pattern strength based on volume and price movement

This pattern often indicates potential upward price movement when the stock breaks out from the handle formation.

## Architecture

- A single collector service runs cron jobs for all stock symbols
- Each stock is collected on a 5-minute schedule
- The API service runs separately in its own container
- All services connect to a shared MySQL database
- All services run within a Docker network

## Limitations

1. The free Alpha Vantage API has rate limits (25 API calls per day)
2. Historical data loading requires additional API calls
3. Pattern detection works best with sufficient historical data

## Adding More Stocks

To add more stocks to the system:

1. Add a new cron job to `crontab.template` for the new stock:
   ```
   # New Stock (NEWSTOCK) - Run at specific minutes
   */5 * * * * cd /app && python3 /app/collect.py NEWSTOCK >> /var/log/cron.log 2>&1
   ```

2. Restart the collector service:
   ```
   docker-compose restart collector
   ```

## Troubleshooting

If you encounter errors:

1. Verify your Alpha Vantage API key is correctly set in the .env file
2. Check Docker logs: `docker-compose logs`
3. Ensure database connections are properly configured

## Prompts Used

This project was developed with assistance from AI tools. The prompts used to guide development can be found in ./prompts/:

- `1 brainstorming with GPT o3.md` - Initial concept development
- `2 cursor agent instructions.md` - Implementation instructions
- `3 debug-iterations.md` - Debugging and optimization iterations