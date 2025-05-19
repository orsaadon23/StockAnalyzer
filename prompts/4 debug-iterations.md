# StockAnalyzer Debugging and Optimization

## Iteration 1: Containerizing API and Adding Scheduled Collection

```
To the docker compose add api as one service.

Create 7 collect tasks that run every 5 minutes each for one of the following companies stocks - Apple, Microsoft, Alphabet, Amazon, Nvidia, Meta and Tesla
```

After receiving this request, I created separate Docker services for the API and collectors. I set up 7 individual collector services, each with its own schedule to collect data for a specific company every 5 minutes.

## Iteration 2: Optimizing Docker Compose Configuration

```
The docker-compose.yml has a lot of repeating code, is there a way to re-use code & variables? for a simpler way to add more stocks later on?
```

I addressed this by implementing YAML anchors and aliases to reduce repetition:
- Created a reusable database config block
- Created a collector base configuration that could be extended
- Simplified the process of adding new stock collectors

This made the docker-compose.yml file significantly shorter and more maintainable.

## Iteration 3: Consolidating Collector Services

```
Can you have it so there are multiple crons but on the same docker, not 7 different ones?
```

I further optimized the architecture by:
- Consolidating 7 separate collector containers into a single container
- Creating a crontab template with scheduled jobs for all stocks
- Updating the start-collector.sh script to handle multiple stocks
- Maintaining the staggered collection schedule to avoid API rate limits

## Debugging Real-World Issues

After implementing the system, I encountered these errors in the logs:

```
For the API container:
ImportError: cannot import name 'url_quote' from 'werkzeug.urls'

For the collector container:
/bin/sh: 1: python: not found
```

These issues were resolved by:
1. Fixing dependency version conflicts in requirements.txt:
   ```
   flask==2.0.1
   werkzeug==2.0.1  # Specify compatible version
   mysql-connector-python==8.0.28
   requests==2.28.1
   ```

2. Correcting the Python path in crontab template:
   ```
   */5 * * * * cd /app && python3 /app/collect.py AAPL >> /var/log/cron.log 2>&1
   ```

3. Adding environment variables to better handle configuration:
   ```yaml
   environment:
     DB_USER: ${DB_USER:-stockuser}
     DB_PASSWORD: ${DB_PASSWORD:-stockpassword}
     ALPHA_VANTAGE_API_KEY: ${ALPHA_VANTAGE_API_KEY:-demo}
   ```

These changes resulted in a more robust, maintainable system that successfully collects and serves stock data. 