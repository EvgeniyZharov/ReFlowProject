import requests
from config import Config
import logging
from config import WB_API_URL, SECRET_KEY, WB_API_CARDS_LIST_URL
from models import *
import psycopg2

logger = logging.getLogger(__name__)


class WBClient:

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = Config.WB_API_URL
        self.headers = {
            'Authorization': SECRET_KEY,
        }
    
    # Проверка соединения
    def connection(self) -> bool:
        res = requests.post(url=self.base_url, headers=self.headers)
        return True if res.connection == '200' else False


    # Получение updatedAt nmID и limit из json
    def create_params(self, res) -> dict:
        limit = int(res['settings']['cursor']['limit'])
        params = {
            'updatedAt': res['settings']['cursor']['updatedAt'],
            'nmID': res['settings']['cursor']['nmID'],
        }
        if limit > 100:
            params['limit'] = limit
        return params

    # Получение всего списка товаров
    def product_list(self,) -> WBCard :
        params = []
        while True:
            res = requests.post(WB_API_CARDS_LIST_URL, params=params)
            result_list = res.json()
            params = self.create_params(result_list)
            if params['total'] <= params['limit'] : # возможно поменять их местами
                break
        return [WBCard(**cart) for cart in result_list]
    
    # Проверка соединения с БД
    def db_connection() -> bool:
        DATABASES = {
            'DB_NAME':'postgres',
            'USER':'user_name',
            'PASSWORD':'password',
            'HOST':'localhost',
            'PORT':'5432',
            'OPTIONS': {
                    'client_encoding': 'UTF8',
                },
            }
        
        try:
            connection = psycopg2.connect(
                host = DATABASES['HOST'],
                database = DATABASES['database'],
                user = DATABASES['user'],
                password = DATABASES['password'],
                )
            return connection
        except Exception as e:
            return f'Connection error {e}'


    # сохранение в БД
    def save_cards(self, WBCard, db):
        if self.db_connection():
            try:
                # проверяем есть ли такой элемент в БД 
                card = WBCard.query.filter_by(
                    account_id = WBCard.account.id,
                    nm_id = WBCard.card_data.get('nmID')
                    ).first()
                
                if card is not None:

                    for card in WBCard:
                        wb_card = WBCard(
                            nm_id=card.get('nmID'),
                            sku=card.get('vendorCode'),
                            name=card.get('title'),
                            price=card.get('price', {}).get('total'),
                            discount=card.get('discount'),
                            brand=card.get('brand'),
                            category=card.get('category'),
                            stocks=card.get('stocks')
                            )
                        wb_size = WBSize(
                            card_id=card.id,
                            size_name=card.get('techSize', ''),
                            size_sku=card.get('skus', [''])[0] if card.get('skus') else '',
                            barcode=card.get('chrtID'),
                    )
                        wb_image = WBImage(
                            card_id=card.id,
                            image_url= card.get('photos'),
                        )

                        db.session.add(wb_card, wb_size, wb_image)
                        
                        saved_count += 1
                        db.session.commit()
                        logger.info(f"Сохранено товаров: {saved_count}")
                        return True
                    else:
                        pass
            except Exception as e:
                db.session.rollback()
                logger.error(f"Ошибка сохранения данных: {e}")
                return 0
        return 'Connection error'


    def validate_api_key_format(api_key):
        return isinstance(api_key, str) and len(api_key) == 64

