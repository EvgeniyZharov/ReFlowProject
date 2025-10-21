from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, DECIMAL
from sqlalchemy.orm import sessionmaker
import os

# Данные для подключения
DB_CONFIG = {
    'dbname': 'reflow_testing',
    'user': 'reflow_user',
    'password': 'reflow_password123',
    'host': '193.162.143.84',
    'port': '5432',
}

# Создание строки подключения
DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"

# Создание engine
engine = create_engine(DATABASE_URL, echo=True)  # echo=True для отладки SQL запросов

# Создание метаданных
metadata = MetaData()

# Определение таблиц
api_keys = Table(
    'api_keys', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(255), nullable=False),
    Column('api_key', String(255), nullable=False),
)

cards = Table(
    'cards', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(255), nullable=False),
    Column('description', Text),
    Column('price', DECIMAL(10, 2)),
)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()


def connection():
    """Тестирование подключения к базе данных"""
    try:
        with engine.connect() as conn:
            print("✅ Успешное подключение к базе данных!")
            return True
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False


def get_all_cards():
    """Получение всех карточек"""
    try:
        with engine.connect() as conn:
            result = conn.execute(cards.select())
            return result.fetchall()
    except Exception as e:
        print(f"Ошибка при получении карточек: {e}")
        return []


def insert_card(title, description, price):
    """Добавление новой карточки"""
    try:
        with engine.connect() as conn:
            stmt = cards.insert().values(
                title=title,
                description=description,
                price=price
            )
            result = conn.execute(stmt)
            conn.commit()
            print(f"✅ Карточка добавлена с ID: {result.inserted_primary_key[0]}")
            return result.inserted_primary_key[0]
    except Exception as e:
        print(f"Ошибка при добавлении карточки: {e}")
        return None


def get_api_keys():
    """Получение всех API ключей"""
    try:
        with engine.connect() as conn:
            result = conn.execute(api_keys.select())
            return result.fetchall()
    except Exception as e:
        print(f"Ошибка при получении API ключей: {e}")
        return []


# Пример использования
if __name__ == "__main__":
    # Тестируем подключение
    connection()

    # Получаем все карточки
    print("\n📋 Все карточки:")
    all_cards = get_all_cards()
    for card in all_cards:
        print(card)

    # Получаем API ключи
    print("\n🔑 API ключи:")
    api_keys_list = get_api_keys()
    for key in api_keys_list:
        print(key)

    # Добавляем новую карточку
    new_card_id = insert_card(
        title="Новая карточка из Python",
        description="Создана через SQLAlchemy",
        price=1999.99
    )