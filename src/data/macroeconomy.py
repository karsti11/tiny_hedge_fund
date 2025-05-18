import pandas as pd
import yfinance as yf
import pandas_datareader.data as web

class MacroDataGetter:
    def __init__(self, config):
        self.config = config
        self.start_date = config.config['start_date']
        self.end_date = config.config['end_date']
        self.commodities_dict = config.config['commodities']

    def fetch_all_data(self):
        self.fed_rates()
        self.us_gdp()
        self.unemployments()
        self.us_cpi()
        self.treasury_yields()
        self.treasury_bonds()
        self.commodities_data()
        
    def merge_macro(self):
        self.macro_data = self.fed_rates.join(
            self.us_gdp, how='left').join(
            self.us_unemp, how='left').join(
            self.eu_unemp, how='left').join(
            self.us_cpi, how='left')
        self.treasury_yields = self.treasury_2y.join(
            self.treasury_10y, how='left')
    
    def fed_rates(self):
        # Monthly interest rates
        self.fed_rates = web.DataReader(
            'FEDFUNDS', 'fred', self.start_date, self.end_date
        ).rename(
            columns={'FEDFUNDS': 'fed_rates'}
        )
    def us_gdp(self):
        # Quarterly US GDP
        self.us_gdp = web.DataReader(
            'GDP', 'fred', self.start_date, self.end_date
        ).rename(
            columns={'GDP': 'us_gdp'}
        )
    def unemployments(self):
        # Monthly unemployment rates
        self.us_unemp = web.DataReader(
            'UNRATE', 'fred', self.start_date, self.end_date
        ).rename(
            columns={'UNRATE': 'us_unemployment_rate'}
        )
        self.eu_unemp = web.DataReader(
            'LRHUTTTTEZM156S', 'fred', self.start_date, self.end_date
        ).rename(
            columns={'LRHUTTTTEZM156S': 'eu_unemployment_rate'}
        )  # Euro Area
    def us_cpi(self):
        # Monthly US CPI data
        self.us_cpi = web.DataReader(
            'CPIAUCSL', 'fred', self.start_date, self.end_date
        ).rename(
            columns={'CPIAUCSL': 'us_cpi'}
        )
    def treasury_yields(self):
        # Daily treasury yield rates
        self.treasury_2y = web.DataReader(
            'DGS2', 'fred', self.start_date, self.end_date
        ).rename(
            columns={'DGS2': 'treasury_2y'}
        )
        self.treasury_10y = web.DataReader(
            'DGS10', 'fred', self.start_date, self.end_date
        ).rename(
            columns={'DGS10': 'treasury_10y'}
        )
    def treasury_bonds(self):
        # Daily treasury bonds prices
        self.treasury_bonds = yf.download(
            'TLT', start=self.start_date, end=self.end_date
        ).rename(
            columns={'TLT': 'treasury_bonds'}
        )
    def commodities_data(self):
        # Daily commodities
        self.commodities_df = pd.DataFrame()
        for name, ticker in self.commodities_dict.items():
            try:
                # Download data using yfinance
                commodity_df = yf.download(ticker, start=self.start_date, end=self.end_date, interval="1d")
                if not commodity_df.empty:
                    commodity_df.columns = [x.lower() for x in commodity_df.columns.get_level_values(0)]
                    commodity_df['commodity'] = name
                    self.commodities_df = pd.concat([self.commodities_df, commodity_df], axis=0)
                    print(f"Successfully fetched data for {name}")
                else:
                    print(f"No data returned for {name}")
            except Exception as e:
                print(f"Error fetching data for {name}: {e}")