import logging
from datetime import timedelta

class Config:
    DEBUG = True
    SECRET_KEY = "fM3PEZwSRcbLkk2Ew82yZFffdAYsNgOddWoANdQo/U3VLZ/qNsOKLsQPYXDPon2t"
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = logging.ERROR  


config_dict = {
    'dev': DevelopmentConfig,
    'pro': ProductionConfig
}
