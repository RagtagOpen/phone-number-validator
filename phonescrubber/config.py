import os

class Config(object):
    def init_app(self):
        return

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class StagingConfig(Config):
    DEBUG = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'demo': ProductionConfig,
    'default': DevelopmentConfig
}
