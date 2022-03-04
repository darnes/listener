from distutils.command.config import config
import os
from tokenize import String


class Config(object):
    config_data = {}

    @property
    def INFLUX_HOST(self):
        return self._from_env('INFLUX_HOST', 'localhost')

    def _from_env(name: String, default=None):
        return os.environ.get(name, default)


# re-consider whenever you'll get any better idea
config = Config()