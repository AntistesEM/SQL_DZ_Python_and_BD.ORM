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
        по id - i, по имени - n:  
''')
if command == 'n':
    for p in session.query(Publisher).filter(Publisher.name.ilike(
            f'{input("Введите имя: ")}')).all():
        print(p)
elif command == 'i':
    for c in session.query(Publisher).filter(
            Publisher.id == f'{input("Введите id: ")}').all():
        print(c)
else:
    print('ОЩИБКА: Введена неверная команда!')

session.close()
