import psycopg2
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, delete_all_tables, Publisher, Book, Shop, Stock, Sale

# Получение данных для подключения к БД
def enter_db_user_credentials():
    print('Введите название базы данных:')
    db = str(input())
    print('Введите логин для доступа к БД:')
    user = str(input())
    print('Введите пароль:')
    password = str(input())   
    return db, user, password

# Наполнение таблиц данными
def import_data_to_bd():
    knigi_v_dom = Publisher(name = 'Книги в каждый дом!')
    knigi_12345 = Publisher(name = 'Книги РАЗ, ДВА, ТРИ, ЧЕТЫРЕ, ПЯТЬ')
    kniga1 = Book(title = 'Турбо Паскаль за две недели!',
                  id_publisher = 1)
    kniga2 = Book(title = 'Сказки, басни, песни и пляски', id_publisher = 2)
    kniga3 = Book(title = 'Полное собрание сочинений Иванова', id_publisher = 2)
    shop1 = Shop(name = 'Книжный на Пушкина')
    shop2 = Shop(name = 'Книжки и пышки')
    stock1 = Stock(id_book = 1, id_shop = 1, count = 10)
    stock2 = Stock(id_book = 1, id_shop = 2, count = 999)
    stock3 = Stock(id_book = 2, id_shop = 1, count = 30)
    sale1 = Sale(price = 100.00, date_sale = '2015-12-29 12:00', id_stock = 1, count = 1)    
    sale2 = Sale(price = 99.99, date_sale = '2016-05-10 12:34', id_stock = 2, count = 2)
    sale3 = Sale(price = 123.99, date_sale = '205-12-30 08:30', id_stock = 3, count = 20)
    session.add_all([knigi_v_dom, knigi_12345, kniga1, kniga2, kniga3, shop1, shop2, 
                    stock1, stock2, stock3, sale1, sale2, sale3])
    session.commit()

def show_shops_by_publisher(publisher_name):
    sq1 = session.query(Publisher).filter(Publisher.name == publisher_name).subquery()
    q1 = session.query(Book).join(sq1, Book.id_publisher == sq1.c.id)
    for b in q1.all():
        q2 = session.query(Shop).join(Stock.shop).filter(Stock.id_book == b.id)
        for sh in q2.all():
            for st in sh.stock:
                q3 = session.query(Sale).filter(Sale.id_stock == st.id)
                for sl in q3.all():
                    print(sl.price, sl.date_sale)
                    str_book_title = '{:<30}'.format(b.title)
                    str_shop_name = '{:<20}'.format(sh.name)
                    str_price = '{:<6}'.format(str(sl.price))
                    print(f'{str_book_title} | {str_shop_name} | {str_price} | {sl.date_sale}')

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
import_data_to_bd()

publishers = ['Издатель 451','Книги в каждый дом!', 'Книги РАЗ, ДВА, ТРИ, ЧЕТЫРЕ, ПЯТЬ']
for publisher in publishers:
    show_shops_by_publisher(publisher)
    print('-----')

session.commit()
session.close()