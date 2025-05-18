I need you to implement the following - 

1. a docker compose that creates a mysql database instance and creates a database calles data with a table "stock" that has 2 columns, timestamp, symbol (string) and price (float). have timestamp+symbol be the key, index by symbol and timestamp. 
if you need sql to do this setup, use additional sql files, used by the setup script. 

2. api.py - a python flask api, simple, that has an api /stock/<SYMBOL> that returns the latest stock price if it exists.

3. collect.py - a minimalistic python script that takes as an argument a stock symbol and fetches the currect stock price of that stock using some free reputable stock api, and stores the result to the sql table above.

Keep the code clean and simple.