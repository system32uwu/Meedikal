from dataclasses import asdict, dataclass
import sqlite3

from flask.wrappers import Request
from util.createDb import getDb

db = getDb()

@dataclass
class BaseModel:
    __tablename__ = 'baseModel'

    @classmethod
    def instantiate(cls,*args):
        return cls(*args)

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
            conditionList = [f"{key} = ?" for key in conditions.keys()]

            values = [v for v in conditions.values()]

        statement = f"""
        SELECT * FROM {cls.__tablename__} 
        {' WHERE ' if len(conditionList) > 0 else ''}
        {f' {logicalOperator} '.join(conditionList) if len(conditionList) > 0 else ''}
        """
        if returns == 'all':
            return [cls(*obj) for obj in db.execute(statement, values).fetchall()]
        else:
            try:
                return cls(*db.execute(statement, values).fetchone())
            except:
                return None

    def save(self):
        attrs = asdict(self).keys()
        values = [v for v in asdict(self).values()]
        
        statement = f"""
        INSERT INTO {self.__tablename__} ({','.join(attrs)})
        VALUES ({",".join("?"*len(values))})
        RETURNING * 
        """ # RETURNING * returns the inserted rows, only works for insert or for virtual tables
        cursor = db.cursor()
        cursor.execute(statement, values)
        result = cursor.fetchone()
        db.commit()
        cursor.close()

        return self.instantiate(*result)

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
    def update(cls, conditions: dict= {}, logicalOperator: str = 'AND'):
        try:
            conditionList = [f"{key} {value.get('operator', '=')} ?"
                            for key, value in conditions.items()]
        except:
            conditionList = [f"{key} = ?"
                            for key in conditions.keys()]

        values = [v.get('value', v)
                 for v in conditions.items()] 

        newValues = [v.get('newValue', v.get('value', v)) 
                    for v in conditions.values()]
        
        values = newValues + values

        statement = f"""
        UPDATE {cls.__tablename__}
        {'SET' if len(conditionList) > 0 else ''}
        {', '.join(conditionList)}
        {'WHERE' f' {logicalOperator} '.join(conditionList) if len(conditionList) > 0 else ''}
        """

        cursor = db.cursor()
        cursor.execute(statement,values)
        db.commit()
        cursor.close()

        for key, value in conditions.items():
            conditions[key] = value.get("newValue", value.get("value"))

        return cls.filter(conditions) # return the affected rows

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