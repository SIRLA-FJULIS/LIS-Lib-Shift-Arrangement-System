import os
basedir = os.path.abspath(os.path.dirname(__file__)) # 獲取目前檔案路徑

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'llsas'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        "sqlite:///" + os.path.join(basedir, 'llsas.db')

config = {
    'development': DevelopmentConfig,

    'default': DevelopmentConfig
}