import requests
from config import Config
import logging
from config import WB_API_URL, SECRET_KEY, WB_API_CARDS_LIST_URL
from models import *
from database import connect_to_db


logger = logging.getLogger()


class WBClient:

    def __init__(
            self, 
            API_KEY : str, 
            ) -> None:
        
        self.API_KEY = API_KEY
        self.base_url = Config.WB_API_URL
        headers = {
            "Authorization": f"Bearer {self.API}",
            "Content-Type": "application/json",
        }
    
    # Проверка соединения
    def connection(self, API, url) -> bool:
        try:
            headers = {
                "Authorization": f"Bearer {API}",
                "Content-Type": "application/json",
            }
            response = requests.get(url=url, headers=headers)
            # Проверяем статус код
            if response.status_code == 200:
                return True
            else:
                logger.exception('Ошибка подключения. API вернул статус код: %s', response.status_code)
                return False
        except Exception as e:
            logger.exception('Ошибка подключения к WB-API %s', e)
            return False


    # Получение updatedAt nmID и limit из json
    '''
    def create_params(res) -> dict:
        try:
            params = {
            'updatedAt': res['settings']['cursor']['updatedAt'],
            'nmID': res['settings']['cursor']['nmID'],
        }
            if res['settings']['cursor']['limit']:
                limit = int(res['settings']['cursor']['limit'])
                if limit > 100:
                    params['limit'] = limit
            return params
        except Exception:
            logger.exception('Ошибка при формировании params')
            return None
'''

    # Получение всего списка товаров
    def product_list(self, api_key, WB_API_CARDS_LIST_URL) -> WBCard :
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        try:
            res = requests.post(WB_API_CARDS_LIST_URL, headers=headers)
            if res.status_code == 200:
                result_list = res.json()
                return [WBCard(**cart) for cart in result_list]
            else:
                logger.exception('Ошибка подключения. API вернул статус код: %s', res.status_code)
        except Exception as e:
            logger.exception('Ошибка при получении карточек: %s', e)
            return None
    

    # Сохранение всего списка товаров в БД
    '''
    def save_product(cards : dict) -> bool:
        try:
            if connect_to_db.connection:
                if cards is not None:
                    for card in cards:

                        card_in_bd = WBCard.query.filter_by(
                        account_id = card.account.id,
                        nm_id = card.card_data.get('nmID')
                        ).first()

                        if not card_in_bd:
                            new_wb_card = WBCard(
                                account_id=WBAccount.account_id,
                                nm_id = card.get('nmID'),
                                sku = card.get('vendorCode'),
                                name = card.get('title'),
                                price = card.get('price', {}).get('total'),
                                discount = card.get('discount'),
                                brand = card.get('brand'),
                                category = card.get('category'),
                                stocks = card.get('stocks')
                                )
                            db.session.add(new_wb_card)

                            for img in card.get('photos'):
                                wb_image = WBImage(
                                    card_id=card.id,
                                    image_url= card.get('photos'),
                                )
                        else:
                            pass
                    return
                else:
                    logger.exception('Пустая карточка')
                    return False
            else:
                logger.exception('Ошибка подключения к БД')
                return False
        except Exception as e:
            logger.exception('Ошибка: %s', e)
            return False
'''

    # Cохранение в БД
    def save_cards(self, WBCards, db):

        if not connect_to_db.connection():
            return 'Connection error'
        try:
            saved_count = 0
            updated_count = 0
            error_count = 0

            for wb_card_data in WBCards:
                # проверяем есть ли такой элемент в БД 
                card = WBCard.query.filter_by(
                    account_id = wb_card_data.account.id,
                    nm_id = wb_card_data.card_data.get('nmID')
                    ).first()
                
                if card is None:
                    
                    # Сохраняем карточку в таблицу WBCard
                    new_wb_card = WBCard(
                        account_id=WBAccount.account_id,
                        nm_id = wb_card_data.get('nmID'),
                        sku = wb_card_data.get('vendorCode'),
                        name = wb_card_data.get('title'),
                        price = wb_card_data.get('price', {}).get('total'),
                        discount = wb_card_data.get('discount'),
                        brand = wb_card_data.get('brand'),
                        category = wb_card_data.get('category'),
                        stocks = wb_card_data.get('stocks')
                        )
                    db.session.add(new_wb_card)
                    
                    # Сохраняем размеры в WBSize
                    wb_size = WBSize(
                        card_id=wb_card_data.id,
                        size_name=wb_card_data.get('techSize', ''),
                        size_sku=wb_card_data.get('skus', [''])[0] if card.get('skus') else '',
                        barcode=wb_card_data.get('chrtID'),
                )
                    db.session.add(wb_size)

                    #
                    wb_image = WBImage(
                        card_id=wb_card_data.id,
                        image_url= wb_card_data.get('photos'),
                    )

                    # Создаем записи об изображениях в WBImage
                    # Создаем записи об изображениях
                    photos = wb_card_data.get('photos', [])
                    for photo_data in photos:
                        # Сохраняем все доступные форматы изображений
                        formats = [
                            ('big', 'Большое изображение'),
                            ('c516x688', 'Среднее изображение 516x688'),
                            ('c246x328', 'Маленькое изображение 246x328'), 
                            ('square', 'Квадратное изображение'),
                            ('tm', 'Миниатюра')
                        ]
                        
                        for format_name, format_description in formats:
                            image_url = photo_data.get(format_name)
                            if image_url:
                                wb_image = WBImage(
                                    card_id=new_wb_card.id,
                                    image_url=image_url,
                                    image_type=format_name,
                                    description=format_description
                                )
                                db.session.add(wb_image)

#                    db.session.add(new_wb_card, wb_size, wb_image)
                    
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




