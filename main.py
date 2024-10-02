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

# Тестирование
def testing():
    knigi_v_dom = Publisher(name = 'Книги в каждый дом!')
    knigi_12345 = Publisher(name = 'Книги РАЗ, ДВА, ТРИ, ЧЕТЫРЕ, ПЯТЬ')
    kniga1 = Book(title = 'Собрание сочинений в 12 томах. Том 1. Пять недель на воздушном шаре. С земли на луну. Вокруг луны (сборник)',
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
    
    q1 = session.query(Publisher).join(Book.publisher)
    for pub in q1.all():
        for b in pub.book:
            sq1 = session.query(Stock).filter(Stock.id_book == b.id).subquery()
            q2 = session.query(Sale).join(sq1, Sale.id_stock == sq1.c.id)
            for s in q2.all():
                print(b.title, ' - ', pub.name, ' - ', s.price, ' - ', s.date_sale)


    # q2 = session.query(Shop).join(Stock.shop)
    # # for sho in subq2.all():
    # #     for sto in sho.stock:
    # #         print(sho.id, sho.name, ' - ', sto.id, sto.count, 'шт.')
    # # subq3 = subq1.join(subq2, subq1.c.id == subq2.c.id_book)

    # subquery1 = q1.subquery()
    # subquery2 = q2.subquery()

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

testing()

session.commit()
session.close()