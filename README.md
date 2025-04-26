# Tiny Hedge Fund
Personal project for better understanding of financial markets.


# Current idea (TODOs):

### 1. Data
#### 1.1. Collecting
- collect data about:
    - macroeconomy (FRED)
    - prices and volumes:
        - stock market (yfinance)
        - comoodities (yfinance)
        - forex (yfinance)
        - crypto (CoinMarketCap, ccxt)
    - volatility
    - news (investigate the best free option for this)
        - check out NewsAPI, Mediastack, Scrape sites like Reuters or Bloomberg using BeautifulSoup or Scrapy, use X posts via the Twitter API
    - economic calendar
        - Scrape or use APIs (e.g., Investing.com’s economic calendar via requests) to collect upcoming events like FOMC meetings or CPI releases
- how can Redis (cache) help there?
- check also sources:
    - Alpha Vantage (stock/forex)
    - Quandl (commodities and some macro)
    - ECB/BOJ APIs (international macro)    


#### 1.2 Storage

- put it all into database (ideally DuckDB) or files (.parquet)
    - recommenation from Grok:
        - Use Parquet for raw and processed data, and DuckDB for querying and feature engineering. Combine both for a hybrid approach (e.g., load Parquet into DuckDB for analysis)
    - Database Alternatives: If DuckDB’s limitations arise (e.g., concurrent writes), consider PostgreSQL with TimescaleDB for time-series data or ClickHouse for high-performance analytics.
- best way to load it incrementally?
    - maintain a metadata table with columns like asset, last_updated and last_timestamp
    - for each asset, fetch only data after last_timestamp using API parameters

#### 1.3 Data Quality
- Add validation scripts to check for missing values, outliers, or duplicate timestamps in fetched data. Use Great Expectations for automated data validation

#### 1.4 Data transformation
- make feature store
- Use a lightweight solution like Feast (open-source) integrated with DuckDB or Parquet files to store and serve features.
- Feature Engineering:
    - Technical: RSI, MACD, VWAP (Volume-Weighted Average Price), SMC, key levels (order blocks, support, resistance)
    - Macro: Lagged CPI, yield curve slope, interest rate changes.
    - Sentiment: News sentiment scores or X post polarity.

#### 1.5 Configuration
- api/secret keys should be handled appropriately
    - .env Files: Store keys in a .env file (e.g., API_KEY=xyz) and load with python-dotenv. Add .env to .gitignore to avoid exposing keys
    - use config.yaml for non-sensitive settings (e.g., API endpoints, update intervals) and load with PyYAML.
### 2. Analysis
#### 2.1 Notebooks
- have all kinds of analyses in nicely structured folders containing notebooks
- check which tools are best for visualising candlesticks or in the beginning just work with line chart of closing prices
    - Plotly: Best for interactive candlestick charts with zoom and hover details. It integrates well with Streamlit and supports OHLC (Open, High, Low, Close) data
    - mplfinance: Specialized for financial visualizations, including candlesticks and technical indicators
- ideas:
    - cross-asset correlations
        - pandas.corr and visualize with seaborn.heatmap
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
    - Use pre-trained models like BERT or FinBERT (from Hugging Face) to summarize news or extract sentiment

### 4. Monitoring
- dashboard for monitoring recent performances of markets and model
- maybe overlapping with analysis dashboard
- save predictions

### Additional ideas:
- Logging: Implement logging (with logging module) to track API calls, errors, and data updates. Store logs in a file or send to a service like Sentry for monitoring.
- Rate Limit Handling: Add logic to respect API rate limits (e.g., using ratelimit library) to avoid bans.
- Alerts: Implement alerts for significant events (e.g., model prediction confidence > 0.9 or price drop > 5%). Use smtplib for email alerts or python-telegram-bot for Telegram notifications.
- Ethical Considerations: Add a DISCLAIMER.md stating that the project is for educational purposes and not financial advice, given the risks of trading.