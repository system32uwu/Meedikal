from dataclasses import asdict, dataclass
from datetime import datetime
import os
import sqlite3

# from util.createDb import db

p = os.path.join(os.path.dirname(__file__))
    
dbPath = f'{p}/../meedikal.db'

db = sqlite3.connect(dbPath)

@dataclass
class User():
    __tablename__ = 'user'
    
    ci: int
    name1: str
    surname1: str
    sex: str
    birthdate: datetime
    location: str
    email: str
    active: bool
    password: str

    name2: str = None
    surname2: str = None
    genre: str = None

def save(obj):
    attrs = asdict(obj).keys()
    values = asdict(obj).values()
    
    statement = f"""
    INSERT INTO {obj.__tablename__} ({','.join(attrs)})
    VALUES ({",".join(["'" + str(v) + "'" for v in values])})
    """
    print(statement)
    db.execute(statement)
    db.commit()

def read(obj):
    conditionList = [f"{key} = '{value}'"
                    for key, value in asdict(obj).items() if value is not None]

    statement = f"""
    SELECT * FROM {obj.__tablename__} WHERE {' AND '.join(conditionList)}
    """
    return db.execute(statement).fetchall()

if __name__ == '__main__':
    a = User(ci=53806188,name1='mateo', surname1='carriqui',sex='M',
             birthdate='2002-10-24', location='Street 123', email='mail@gmail.com',
             active=True, password='123')
    save(obj=a)
    print(read(a))