import datetime

class BaseConfig(object):
    # Database
    # Slash needs percent encoding
    MONGO_URI = "mongodb://deepIoAdmin:2019%2FRoussy@localhost:27017/deepio"
    
    # Token Authentication
    JWT_SECRET_KEY = 'SOOO_SECRET'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=120)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']
    
    # Development vs production environment
    DEBUG = True
    
    # Mail Client - all default, need to be changed to actual mail server
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = None
    MAIL_MAX_EMAILS = None
    MAIL_ASCII_ATTACHMENTS = False