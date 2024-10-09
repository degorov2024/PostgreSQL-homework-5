import json
import psycopg2
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import (create_tables, delete_all_tables, Publisher, Book, Shop, 
                    Stock, Sale)

# Получение данных для подключения к БД
def enter_db_user_credentials():
    print('Введите название базы данных PostgreSQL.\nБудьте внимательны! \
Из БД будут предварительно удалены ВСЕ таблицы!')
    db = str(input())
    print('Введите логин для доступа к БД:')
    user = str(input())
    print('Введите пароль:')
    password = str(input())   
    return db, user, password

# Импорт данных в БД из файла json
def import_data_to_bd(file):
    with open(file, 'r') as fd:
        data = json.load(fd)
    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()

# Вывод данных в формате:
# название книги | название магазина | стоимость покупки | дата покупки
def show_shops_by_publisher(publisher_name):
    q_shops = (session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)
               .select_from(Shop).join(Stock).join(Book).join(Publisher)
               .join(Sale))
    #Проверка, id на входе или название издателя
    if publisher_name.isdigit():
        q_result = q_shops.filter(Publisher.id == publisher_name).all()
    else:
        q_result = q_shops.filter(Publisher.name == publisher_name).all()
    #Вывод данных, если они есть
    if q_result == []:
        print('Ничего не найдено...')
    else:
        for book, shop, price, sold_date in q_result:
            print(f"{book: <40} | {shop: <12} | {price: <8} | "
                  f"{sold_date.strftime('%d-%m-%Y')}")


#Подключение к БД, создание сессии
db, user, password = enter_db_user_credentials()
DSN = f'postgresql://{user}:{password}@localhost:5432/{db}'
engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind = engine)
session = Session()

#УДАЛЕНИЕ ВСЕХ ТАБЛИЦ ИЗ БД - для удобства тестирования
delete_all_tables(engine)
#создание таблиц
create_tables(engine)

#Наполнение таблиц данными
import_data_to_bd('fixtures/tests_data.json')

print('Введите имя издателя или его id:')
publisher = str(input())
print('-----')
show_shops_by_publisher(publisher)

session.commit()
session.close()