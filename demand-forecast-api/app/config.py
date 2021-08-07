from typing import Dict, Literal, TypedDict
from utils.config_utils import get_config_file
from flask.app import Flask


class DefaultConfig:
    JSON_SORT_KEYS = False
    
    @staticmethod
    def init(app: Flask):
        ext_configs = get_config_file()
        app.config.update(**ext_configs)


class DevConfig(DefaultConfig):
    DEBUG = True


class ProductionConfig(DefaultConfig):
    ENV = 'production'
    DEBUG = False


class ConfigDict(TypedDict):
    DEV: DevConfig
    PRODUCTION: ProductionConfig


envirioments_config = ConfigDict(
    DEV=DevConfig,
    PRODUCTION=ProductionConfig
)
