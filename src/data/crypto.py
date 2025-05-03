import yfinance as yf
import pandas_datareader.data as web

class MacroDataGetter:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def fetch_all_data(self):
        self.fed_rates()
        self.us_gdp()
        self.unemployments()
        self.us_cpi()
        self.treasury_yields()
        self.treasury_bonds()
        self.commodities()
        self.sp500()
    
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
    def commodities(self):
        # Daily commodities
        self.gold = yf.download('GC=F', start=self.start_date, end=self.end_date)  # Gold futures
        self.silver = yf.download('SI=F', start=self.start_date, end=self.end_date)  # Silver futures
        self.copper = yf.download('HG=F', start=self.start_date, end=self.end_date)  # Copper futures
        self.oil = yf.download('CL=F', start=self.start_date, end=self.end_date) # WTI Crude futures

    def sp500(self):
        self.sp500 = yf.download("^GSPC", start=self.start_date, end=self.end_date, interval="1d")