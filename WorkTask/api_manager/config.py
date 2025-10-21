import os
import logging

def configurete_logging():
    logging.basicConfig(
        level=logging.INFO, # level
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)s:%(lineno)d %(levelname)s - %(message)s",
    )

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///wb_api.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    API = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjUwOTA0djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTc3NDQyODQ3NiwiaWQiOiIwMTk5Nzg1NS00MDI2LTc3OTYtODVlOC0xYjVlMzA3NzZiNzYiLCJpaWQiOjIxNzM2NjAzLCJvaWQiOjQ0MTM4MjQsInMiOjAsInNpZCI6ImE2YjI4ZmM3LTNhNTYtNDljYy1iYjRjLWNlY2UzOWU0MWNhNCIsInQiOnRydWUsInVpZCI6MjE3MzY2MDN9.EKjZheLffiVyfvTIoHRWk3Od4SAWho77PKLuS53t2mGIbsF8Lfsx6R7Zj-o-KxHgA8AshIOqAgWxw8agyvfSJA'


    WB_API_URL = 'https://business-api.wildberries.ru/api/v1'
    WB_API_CARDS_LIST_URL = 'https://content-api.wildberries.ru/content/v2/get/cards/list'


    LOG_LEVEL = 'INFO'



