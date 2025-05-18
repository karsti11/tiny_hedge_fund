import json
import pandas as pd
from requests import Session
import yfinance as yf

class CryptoData:
    def __init__(
        self, 
        config,
        top_cryptos_num,
        ohlcv_cols
    ):
        self.config = config
        self.cmc_apikey = self.config.config['cmc_apikey']
        self.crypto_symbols_correction = self.config.config['crypto_symbols_correction']
        self.todays_date_str = self.config.config['todays_date_str']
        self.start_date = self.config.config['start_date']
        self.end_date = self.config.config['end_date']
        self.raw_data_folder = self.config.config['raw_data_folder']
        self.top_cryptos_num = top_cryptos_num
        self.ohlcv_cols = ohlcv_cols
        self.ohlc_cols = ohlcv_cols[:-1]
        self.volume_col = ohlcv_cols[-1]
        self.calculate_crypto_data()
        
    def calculate_crypto_data(self):
        self.cryptocurrencies_prices_data()
        self.calculate_crypto_market_cap()
    
    def top_cryptos_by_market_cap(self):
        
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        parameters = {
           'start':'1',
           'limit': str(self.top_cryptos_num),
           'convert':'USD'
        }
        headers = {
           'Accepts': 'application/json',
           'X-CMC_PRO_API_KEY': self.cmc_apikey,
        }
        session = Session()
        session.headers.update(headers)
        
        try:
          response = session.get(url, params=parameters)
          data = json.loads(response.text)
          #print(data)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
          print(e)
        
        # exclude stablecoins
        self.cmc_coin_dict = {}
        for coin in data['data']:            
            if coin['cmc_rank'] < self.top_cryptos_num and 'stablecoin' not in coin['tags']:
                #self.cmc_coin_list.append(coin['symbol'])
                if coin['symbol'] in self.crypto_symbols_correction:
                    self.cmc_coin_dict[self.crypto_symbols_correction[coin['symbol']]] = coin['quote']['USD']['market_cap']
                else:
                    self.cmc_coin_dict[coin['symbol']] = coin['quote']['USD']['market_cap']
            
        return self.cmc_coin_dict

    def cryptocurrencies_prices_data(self):
        self.cmc_coin_dict = self.top_cryptos_by_market_cap()
        self.all_crypto_prices = pd.DataFrame()
        for symbol, market_cap in self.cmc_coin_dict.items():
            ticker = f'{symbol}-USD'
            crypto_prices = yf.download(ticker, start=self.start_date, end=self.end_date)
            crypto_prices['last_market_cap'] = market_cap
            if crypto_prices.shape[0] >= 1:
                crypto_prices.columns = [x.lower() for x in crypto_prices.columns.get_level_values(0)]
                crypto_prices['ticker'] = ticker
                # Calculate market cap for each record from last market cap 
                for col in self.ohlc_cols:
                    crypto_prices.loc[:, f'{col}_scaled'] = crypto_prices[col]/crypto_prices[col].values[-1]
                    crypto_prices.loc[:, f'{col}_market_cap'] = crypto_prices.loc[:, f'{col}_scaled']*market_cap
                self.all_crypto_prices = pd.concat([self.all_crypto_prices, crypto_prices], axis=0)
            else:
                continue
        return self

    def calculate_crypto_market_cap(self):
        market_cap_cols = [f'{x}_market_cap' for x in self.ohlc_cols]
        pivot_crypto_market_cap = self.all_crypto_prices.reset_index().pivot(
            index='Date', 
            columns='ticker', 
            values=market_cap_cols
        )
        # TOTAL
        self.total_market_cap_df = pd.concat([pivot_crypto_market_cap[col].sum(axis=1) for col in market_cap_cols], axis=1)
        self.total_market_cap_df.columns = market_cap_cols
        # for col in market_cap_cols:
        #     candle_part_market_cap = pivot_crypto_market_cap.loc[:, (pivot_crypto_market_cap.columns.get_level_values(0) == col)].sum(axis=1)
        #     candle_part_market_cap.name = col
        #     self.total_market_cap_df = pd.concat([self.total_market_cap_df, candle_part_market_cap], axis=1)
        # TOTAL2 - Excluding BTC
        pivot_for_total2 = pivot_crypto_market_cap.loc[:, (pivot_crypto_market_cap.columns.get_level_values(0) != 'BTC-USD')]
        self.total2_market_cap_df = pd.concat([pivot_for_total2[col].sum(axis=1) for col in market_cap_cols])
        self.total2_market_cap_df.columns = market_cap_cols
        # TOTAL3 - Excluding BTC and ETH-USD
        pivot_for_total3 = pivot_crypto_market_cap.loc[:, ~(pivot_crypto_market_cap.columns.get_level_values(0).isin(['BTC-USD', 'ETH-USD']))]
        self.total3_market_cap_df = pd.concat([pivot_for_total3[col].sum(axis=1) for col in market_cap_cols])
        self.total3_market_cap_df.columns = market_cap_cols
        
        return self
    
    def save_data(self):
        try:
            self.market_indexes_df.to_parquet(self.raw_data_folder / f'stock_market_indexes_{self.todays_date_str}.parquet')
        except Exception as e:
                print(f"Error saving all macro data: {e}")