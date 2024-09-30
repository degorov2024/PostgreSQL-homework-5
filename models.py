import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=100), unique=True)
    #т.к., к примеру, для отчетов ПФР в названиях организаций ограничение 100 символов

class Book(Base):
    __tablename__ = "book"
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=110), nullable=False)
    #Пример - Собрание сочинений в 12 томах. Том 1. Пять недель на воздушном шаре. С земли на луну. Вокруг луны (сборник)
    #не уникально, т.к. могут быть переиздания, выпуски др. издательствами...
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable = False)

    publisher = relationship(Publisher, backref="book") #--------------------------------backref="books"?

class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=100), unique=True)

# class Stock(Base):
#     __tablename__ = "stock"


# class Sale(Base):
#     __tablename__ = "sale"

def create_tables(engine):
    Base.metadata.create_all(engine)