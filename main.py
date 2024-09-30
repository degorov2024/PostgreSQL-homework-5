import psycopg2
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop

# Получение данных для подключения к БД
def enter_db_user_credentials():
    print('Введите название базы данных:')
    db = str(input())
    print('Введите логин для доступа к БД:')
    user = str(input())
    print('Введите пароль:')
    password = str(input())   
    return db, user, password

#Подключение к БД, создание сессии
db, user, password = enter_db_user_credentials()
DSN = f'postgresql://{user}:{password}@localhost:5432/{db}'
engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind = engine)
session = Session()

create_tables(engine)

knigi_v_dom = Book(title = 'Книги в каждый дом!')
print(knigi_v_dom.id)

session.add(knigi_v_dom)
session.commit()

print('id издателя:' + knigi_v_dom.id)

session.close()