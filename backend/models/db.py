from dataclasses import asdict, dataclass
import sqlite3

from flask.wrappers import Request
from util.createDb import getDb

db = getDb()

@dataclass
class BaseModel:
    __tablename__ = 'baseModel'

    @classmethod
    def query(cls):
        return [cls(*row) for row in 
        db.execute(f"SELECT * FROM {cls.__tablename__}")]

    @classmethod # dict shape: {'key': 'value'} || {'key': {'value': 'v', 'operator': '='}}
    def filter(cls, conditions: dict= {}, logicalOperator: str = 'AND', returns='all'):
        try:
            conditionList = [f"{key} {value.get('operator', '=')} ?"
                        for key, value in conditions.items()]

            values = [v.get('value', None) for v in conditions.values() 
                    if v is not None]
        except:
            conditionList = [f"{key} = ?"
                        for key in conditions.keys()]

            values = [v for v in conditions.values()]

        statement = f"""
        SELECT * FROM {cls.__tablename__} 
        {' WHERE ' if len(conditionList) > 0 else ''}
        {f' {logicalOperator} '.join(conditionList) if len(conditionList) > 0 else ''}
        """
        if returns == 'all':
            return [cls(**obj) for obj in db.execute(statement, values).fetchall()]
        else:
            try:
                return cls(*db.execute(statement, values).fetchone())
            except:
                return None

    def save(self, fetchBeforeReturn=False):
        attrs = asdict(self).keys()
        values = [v for v in asdict(self).values()]
        
        statement = f"""
        INSERT INTO {self.__tablename__} ({','.join(attrs)})
        VALUES ({",".join("?"*len(values))})
        """

        db.cursor().execute(statement, values)
        db.commit()

        return self

    @classmethod
    def delete(cls, conditions: dict= {}, logicalOperator: str = 'AND'):
        try:
            conditionList = [f"{key} {value.get('operator', '=')} ?"
                        for key, value in conditions.items()]

            values = [v.get('value', None) for v in conditions.values() 
                    if v is not None]
        except:
            conditionList = [f"{key} = ?"
                        for key in conditions.keys()]

            values = [v for v in conditions.values()]

        statement = f"""
        DELETE FROM {cls.__tablename__} 
        {' WHERE ' if len(conditionList) > 0 else ''}
        {f' {logicalOperator} '.join(conditionList) if len(conditionList) > 0 else ''}
        """

        db.execute(statement,values)
        db.commit()

        return True

    @classmethod
    def update(cls, conditions: dict= {}, request:Request=None, logicalOperator: str = 'AND'):
        conditionList = [f"{key} {value.get('operator', '=')} ?"
                        for key, value in conditions.items()]

        values = [v.get('value', None) for v in conditions.values() 
                 if v is not None and request.method != 'PUT'] # PUT replaces, even if value is null.

        newValues = [v.get('newValue', v.get('value', None)) for v in conditions.values() 
                    if v is not None and request.method != 'PUT'] # PUT replaces, even if value is null.
        
        values = values + newValues

        statement = f"""
        UPDATE {cls.__tablename__}
        {'SET' if len(conditionList) > 0 else ''}
        {', '.join(conditionList)}
        {'WHERE' if len(conditionList) > 0 else ''}
        {f'{logicalOperator} '.join(conditionList) if len(conditionList) > 0 else ''}
        """

        db.execute(statement,values)
        db.commit()

        return cls.filter(conditions)

# examples:

# from models.User import User

# u = User(53806188,'mateo',None,'carriqui',None,'M',None,'2002-10-24',
#         'Street 123', 'gmail@gmail.com', 'jaja123', True)

# u.save()

# conditions = {'ci': {
#         'value': 53806188,
#         'operator': '='
#         }}

# data = User.filter(conditions)

# print(data)