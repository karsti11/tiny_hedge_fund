import pandas as pd
import yfinance as yf

class StockMarketData:
    def __init__(
        self,
        config
    ):
        self.config = config
        self.start_date = config.config['start_date']
        self.end_date = config.config['end_date']
        self.market_indexes = config.config['stocks']['indexes']
        self.todays_date_str = config.config['todays_date_str']

    def load_market_indexes(self):
        self.market_indexes_df = pd.DataFrame()
        for name, ticker in self.market_indexes.items():
            try:
                # Download data using yfinance
                index_df = yf.download(ticker, start=self.start_date, end=self.end_date, interval="1d")
                if not index_df.empty:
                    index_df.columns = [x.lower() for x in index_df.columns.get_level_values(0)]
                    index_df['market_index'] = name
                    self.market_indexes_df = pd.concat([self.market_indexes_df, index_df], axis=0)
                    print(f"Successfully fetched data for {name}")
                else:
                    print(f"No data returned for {name}")
            except Exception as e:
                print(f"Error fetching data for {name}: {e}")
                
    def save_data(self, raw_data_folder):
        try:
            self.market_indexes_df.to_parquet(raw_data_folder / f'stock_market_indexes_{self.todays_date_str }.parquet')
        except Exception as e:
                print(f"Error saving all macro data: {e}")