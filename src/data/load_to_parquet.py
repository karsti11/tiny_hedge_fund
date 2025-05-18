from src.config import Config
from src.data.macroeconomy import MacroDataGetter
from src.data.crypto import CryptoData
from src.data.stocks import StockMarketData


class CollectData:
    def __init__(self):
        self.config = Config()
        self.start_date = self.config.config['start_date']
        self.end_date = self.config.config['end_date']
        self.raw_data_folder = self.config.config['raw_data_folder']
        self.cmc_apikey = self.config.config['cmc_apikey']
        self.todays_date_str = self.config.config['todays_date_str']
        self.collect_data()
        self.save_data()

    def collect_data(self):
        self.collect_macro_data()
        self.collect_stock_market_data()
        self.collect_crypto_data()
    
    def save_data(self):
        self.save_macro_data()
        self.save_stock_market_data()
        self.save_crypto_data()
        self.save_crypto_market_cap()

    def collect_macro_data(self):
        self.macro_data = MacroDataGetter(config=self.config)
        self.macro_data.fetch_all_data()
        self.macro_data.merge_macro()
        self.commodities_data = self.macro_data.commodities_data

    def collect_stock_market_data(self):
        self.stock_market_data = StockMarketData(config=self.config)
        self.stock_market_data.load_market_indexes()
    
    def collect_crypto_data(self):
        self.crypto_data = CryptoData( 
            config=self.config,
            top_cryptos_num=50,
            ohlcv_cols=['open', 'high', 'low', 'close', 'volume']
        )

    def save_data(self):
        filenames = [
            ("macros", self.macro_data.macro_data),
            ("market_indices", self.stock_market_data.market_indexes_df),
            ("commodities", self.macro_data.commodities_df),
            ("crypto_prices", self.crypto_data.all_crypto_prices),
            ("crypto_market_cap", self.crypto_data.total_market_cap_df),
            ("crypto_market_cap_excl_btc", self.crypto_data.total2_market_cap_df),
            ("crypto_market_cap_excl_btc_eth", self.crypto_data.total3_market_cap_df),
        ]

        for filename, data in filenames:
            try:
                data_savepath = self.raw_data_folder / f'{filename}_{self.todays_date_str}.parquet'
                data.to_parquet(data_savepath)
                print(f"{data_savepath} saved successfully.")
            except Exception as e:
                print(f"Error saving {data_savepath}: {e}")
