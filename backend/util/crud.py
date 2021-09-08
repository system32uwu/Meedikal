from dataclasses import asdict
from typing import Any

from flask.json import jsonify
from .createDb import getDb

db = getDb()

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

    db.execute(statement,values)
    db.commit()
    return newObj

def crudReturn(result:Any=None):
    return jsonify({"result": result}), 200