import os
import yaml
from datetime import datetime
from dotenv import load_dotenv
from src.utils import get_project_root


class Config:

    def __init__(self, 
                 target_file=get_project_root() / 'src/config/main.yaml'
                 ):
        self.file = target_file
        self.load_yaml_config()
        self.add_dynamic_config()
        self.add_api_keys()

    def load_yaml_config(self):
        with open(self.file, 'r') as file:
            self.config = yaml.safe_load(file)
        print(self.config)

    def add_dynamic_config(self):
        self.config['todays_date_str'] = datetime.now().date().strftime('%d%m%Y')
        self.config['start_date'] = datetime(1990, 1, 1)
        self.config['end_date'] = datetime.now().date()
        self.config['project_root'] = get_project_root()
        self.config['raw_data_folder'] = self.config['project_root'] / 'data/raw'

    def add_api_keys(self):
        load_dotenv()
        self.config['cmc_apikey'] = os.getenv('CMC_APIKEY')
