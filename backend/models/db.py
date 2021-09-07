from dataclasses import asdict, dataclass
from datetime import datetime
import sqlite3
# from util.createDb import getDb

# db = getDb()

import os

p = os.path.join(os.path.dirname(__file__))
    
dbPath = f'{p}/../meedikal.db'

getDb = lambda: sqlite3.connect(dbPath)

db = getDb()

@dataclass
class User():
    __tablename__ = 'user'
    
    ci: int
    name1: str
    name2: str
    surname1: str
    surname2: str
    sex: str
    genre: str
    birthdate: datetime
    location: str
    email: str
    active: bool
    password: str

    @classmethod
    def getByCi(cls, ci:int):
        return User(*db.execute(f"SELECT * FROM {cls.__tablename__} WHERE ci=?", [ci]).fetchone())

def save(obj):
    attrs = asdict(obj).keys()
    values = [v for v in asdict(obj).values()]
    
    statement = f"""
    INSERT INTO {obj.__tablename__} ({','.join(attrs)})
    VALUES ({",".join("?"*len(values))})
    """

    try:
        db.execute(statement, values)
        db.commit()
        return obj, True
    except Exception as exc:
        print(f'exc: {exc}')
        return obj, False

def read(obj):
    conditionList = [f"{key} = ?"
                    for key, value in asdict(obj).items() if value is not None]

    values = [v for v in asdict(obj).values()]

    statement = f"""
    SELECT * FROM {obj.__tablename__} WHERE {' AND '.join(conditionList)}
    """
    return db.execute(statement, values).fetchall()

def update(oldObj, newObj):
    conditionList = [f"{key} = ?"
                    for key in asdict(oldObj).keys()]

    values = [
             newV for newV in asdict(newObj).values()] + [
             oldV for oldV in asdict(oldObj).values()
             ]

    statement = f"""
    UPDATE {newObj.__tablename__}
    SET {', '.join(conditionList)}
    WHERE {' AND '.join(conditionList)}
    """

    try:
        db.execute(statement,values)
        db.commit()
        return newObj, True
    except Exception as exc:
        print(f"exc: {exc}")
        return newObj, False