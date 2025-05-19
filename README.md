# StockAnalyzer

A system to collect and serve stock price data for major tech companies with pattern detection capabilities.

## Quick Start

1. Get your free Alpha Vantage API key from https://www.alphavantage.co/support/#api-key
2. Create a `.env` file in the project root:
   ```
   ALPHA_VANTAGE_API_KEY=your_api_key
   DB_USER=stockuser
   DB_PASSWORD=stockpassword
   ```
3. Start the system:
   ```
   docker-compose up -d
   ```

## Usage

### Get Latest Stock Price
```
curl http://localhost:5000/stock/AAPL
```

### Check for Cup and Handle Pattern
```
curl http://localhost:5000/cup-and-handle/AAPL
```

Supported stock symbols: AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA

## Development

This project was developed with AI assistance. The full conversation history and prompts used can be found in the `./prompts/` directory:

- `1 brainstorming with GPT o3.md` - Initial concept development
- `2 cursor agent instructions.md` - Implementation instructions
- `3 adding the cup and handle pattern.md` - Pattern detection implementation
- `4 debug-iterations.md` - Debugging and optimization iterations