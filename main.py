import json
import psycopg2
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, delete_all_tables, Publisher, Book, Shop, Stock, Sale

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
    #все книги конкретного издателя
    sq1 = session.query(Publisher).filter(Publisher.name == publisher_name).subquery()
    q1 = session.query(Book).join(sq1, Book.id_publisher == sq1.c.id)
    for b in q1.all():
        #магазины, в которых есть конкретная книга
        q2 = session.query(Shop).join(Stock.shop).filter(Stock.id_book == b.id)
        for sh in q2.all():
            #продажи книги из инвентаря магазина
            sq2 = session.query(Stock).filter(Stock.id_book == b.id, 
                                              Stock.id_shop == sh.id).subquery()
            q3 = session.query(Sale).join(sq2, Sale.id_stock == sq2.c.id)
            for sl in q3.all():
                str_book_title = '{:<40}'.format(b.title)
                str_shop_name = '{:<12}'.format(sh.name)
                str_price = '{:<6}'.format(str(sl.price))
                print(f'{str_book_title} | {str_shop_name} | {str_price} \
| {sl.date_sale}')


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

print('Введите имя издателя:')
publisher = str(input())
print('-----')
show_shops_by_publisher(publisher)

# publishers = ['O’Reilly','Pearson', 'Microsoft Press', 'No starch press']
# for publisher in publishers:
#     show_shops_by_publisher(publisher)
#     print('-----')

session.commit()
session.close()