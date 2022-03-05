import json
import os
import logging

import yaml


log = logging.getLogger(__name__)

class Config(object):
    config_data = {}

    @classmethod
    def load_config(cls):
        config_filename = cls._from_env('CONFIG_FILE', '~/config.yml')
        log.info('using config file `%s`', config_filename)
        with open(config_filename, 'r') as config_file:
            config_data = yaml.full_load(config_file)
            # todo: add some masking to the security configs
            log.debug('config data %s', json.dumps(config_data))
            return config_data

    def __init__(self) -> None:
        self.config_data = self.load_config()

    @property
    def INFLUX_HOST(self):
        return self._from_env('INFLUX_HOST', 'localhost')

    @staticmethod
    def _from_env(name: str, default=None):
        return os.environ.get(name, default)

    @property
    def OANDA(self):
        return self.config_data.get('oanda', {})

    @property
    def OANDA_TOKEN(self):
        return self.OANDA.get('TOKEN')

    @property
    def OANDA_STREAM_HOST_NAME(self):
        return  self.OANDA.get('STREAM_HOST_NAME')

    @property
    def OANDA_ACCOUNT_ID(self):
        return self.OANDA.get('ACCOUNT_ID')

# re-consider whenever you'll get any better idea
config = Config()