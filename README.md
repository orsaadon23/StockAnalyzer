# StockAnalyzer

A system to collect and serve stock price data for major tech companies.

## Components

1. MySQL database - Stores stock price data with timestamp, symbol, and price
2. Flask API - Provides an endpoint to retrieve the latest stock price
3. Collector Service - A single service that collects price data for multiple stocks on different schedules:
   - Apple (AAPL)
   - Microsoft (MSFT)
   - Alphabet/Google (GOOGL)
   - Amazon (AMZN)
   - Nvidia (NVDA)
   - Meta (META)
   - Tesla (TSLA)

## Setup

1. **IMPORTANT**: Get your free Alpha Vantage API key:
   - Go to https://www.alphavantage.co/support/#api-key
   - Register for a free API key (takes less than 20 seconds)
   - Create a .env file and set your API key:
   
   .env
   ```
   ALPHA_VANTAGE_API_KEY=your_api_key
   ```
   
   **Note**: Without setting a valid API key, most requests will fail with a demo key limitation error.

2. Start all services:
   ```
   docker-compose up -d
   ```

## Usage

Retrieve the latest stock price for a company:
```
curl http://localhost:5000/stock/AAPL  
# Replace AAPL with any supported symbol
```

Check the Cup and Handle:
```
curl http://localhost:5000/cup-and-handle/AAPL  
# Replace AAPL with any supported symbol
```

## Architecture

- A single collector service runs cron jobs for all stock symbols
- Each stock is collected on a 5-minute schedule
- The API service runs separately in its own container
- All services connect to a shared MySQL database
- All services run within a Docker network

## Limitations

1. Rate Limit for API if a lot of stocks are handled, add staggered requests.

## Adding More Stocks

To add more stocks to the system:

1. Add a new cron job to `crontab.template` for the new stock:
   ```
   # New Stock (NEWSTOCK) - Run at specific minutes
   /bin/user/python /app/collect.py NEWSTOCK >> /var/log/cron.log 2>&1
   ```

3. Restart the collector service:
   ```
   docker-compose restart collector
   ```