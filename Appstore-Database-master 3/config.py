# config.py

# DATABASE: appstore_admin_db
# USER: appstore_admin@localhost
# PASSWORD: appstore12345

#
class Config(object):
    """
    Common configurations
    """
    DEBUG = True
    # Put any configurations here that are common across all environments


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = True

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}