import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///wb_api.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    WB_API_URL = 'https://business-api.wildberries.ru/api/v1'
    WB_API_CARDS_LIST_URL = 'https://content-api.wildberries.ru/content/v2/get/cards/list'


    LOG_LEVEL = 'INFO'



