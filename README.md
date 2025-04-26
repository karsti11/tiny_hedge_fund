# Tiny Hedge Fund
Personal project for better understanding of financial markets.


# Current idea (TODOs):

### 1. Data
#### 1.1. Collecting
- collect data about:
    - macroeconomy (yfinance)
    - prices and volumes:
        - stock market (yfinance)
        - comoodities (yfinance)
        - forex (yfinance)
        - crypto (CoinMarketCap, ccxt)
    - news (investigate the best free option for this)
- how can Redis (cache) help there?
- best way to load it incrementally?

#### 1.2 Storage
- make feature store
- put it all into database (ideally DuckDB) or files (.parquet)

#### 1.3 Configuration
- api/secret keys should be handled appropriately
### 2. Analysis
#### 2.1 Notebooks
- have all kinds of analyses in nicely structured folders containing notebooks
- check which tools are best for visualising candlesticks or in the beginning just work with line chart of closing prices
- ideas:
    - map historical events to macroeconomic charts
        - might be visualised in dashboard, collect events in one table 
    - relation of volume/relative volume changes in comparison to price (at key levels)
        - relative volume paired/visualised with key price levels (find trend change moments)
    - where does volume stand in comparison to its historical data distribution (mark/color by standard deviations)?
    - how price changed historically when certain relative volume appeared?

#### 2.2 Dashboard
- after some analyses start with first version of dashboard which will automate repeated analyses

### 3. Modelling
- after satisfying amount of analyses and first dashboard is made try to come up with first some rule-based model
- use AI/ML only when clear benefit is shown (compare with rule-based as baseline)
- use LLMs maybe news summarization

### 4. Monitoring
- dashboard for monitoring recent performances of markets and model
- maybe overlapping with analysis dashboard
- save predictions