import os 

class Config(object):
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    
    SQLALCHEMY_DATABASE_URI = "mysql://root:"+os.getenv("DB_ROOT_PASSWORD")+"@db:3306/"+os.getenv("DB_NAME")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')   
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')



class ProductionConfig(Config):
    FLASK_ENV = 'production'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
