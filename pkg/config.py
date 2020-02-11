"""Persistent configuration"""
import logging
from gateway_addon import Database

class Config(Database):
    def __init__(self, package_name):
        Database.__init__(self, package_name, None)
        self.timezone = None
        self.lat = None
        self.lng = None
        self.horizon = None
        self.sunset_offset_mins = None
        self.sunrise_offset_mins = None        
        self.log_level = None
        self.open()
        self.load()

    def load(self):
        try:
            config = self.load_config()
            # config = json.loads(config.decode('utf-8'))
            logging.info('config %s', config)
            self.timezone = config['timezone']
            self.lat = config['lat']
            self.lng = config['lng']
            self.horizon = config['horizon']
            self.sunset_offset_mins = config['sunset_offset_mins']
            self.sunrise_offset_mins = config['sunrise_offset_mins']         
            self.log_level = config['log_level']
        except Exception as ex:
            logging.exception('Strange config', config)
