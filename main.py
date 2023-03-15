import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Stock, Shop, Sale
import os

FILE_NAME = 'test.json'
FILE_DIR = 'fixtures'
ROOT_PATH = os.getcwd()
full_path_to_file = os.path.join(ROOT_PATH, FILE_DIR, FILE_NAME)

sql_system = 'postgresql'
login = 'postgres'
password = input('Введите пароль: ')
host = 'localhost'
port = '5432'
db_name = 'sql_dz_6_orm'
DSN = f'{sql_system}://{login}:{password}@{host}:{port}/{db_name}'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()
create_tables(engine)

with open(full_path_to_file, 'r') as file:
    data = json.load(file)
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

command = input('''Для поиска издателя укажите параметр поиска:
        по id - i, по имени - n: ''')
input_ = input('Ведите значение параметра: ')
print('Название книги'.ljust(50), 'Название магазина'.center(20),
      'Стоимость покупки'.center(20), 'Дата покупки'.rjust(13))
if command == 'i':
    for c in session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).\
            join(Sale.stock).join(Stock.shop).join(Stock.book).\
            filter(Book.id_publisher == input_).all():
        print(f'{list(c)[0].ljust(50)}{list(c)[1].center(20)}'
              f'{str(list(c)[2]).center(23)}{str(list(c)[3]).center(13)}')
elif command == 'n':
    id_ = session.query(Publisher.id).filter(Publisher.name == input_).all()[0]
    for c in session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).\
            join(Sale.stock).join(Stock.shop).join(Stock.book).\
            filter(Book.id_publisher == id_[0]).all():
        print(f'{list(c)[0].ljust(50)}{list(c)[1].center(20)}'
              f'{str(list(c)[2]).center(23)}{str(list(c)[3]).center(13)}')
else:
    print('ОЩИБКА: Введена неверная команда!')

session.close()
