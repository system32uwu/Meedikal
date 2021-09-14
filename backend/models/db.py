from dataclasses import asdict, dataclass
import sqlite3

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
        conditionList = []
        values = []
        
        if conditions is not None:
            for k,v in conditions.items():
                if isinstance(v,dict):
                    operator = v.get('operator', '=')
                    value = v.get('value')
                else:
                    operator = '='
                    value = v

                conditionList.append(f"{k} {operator} ?")

                values.append(value)

        statement = f"""
        SELECT * FROM {cls.__tablename__} 
        {'WHERE ' + f' {logicalOperator} '.join(conditionList) if len(conditionList) > 0 else ''}
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

    def saveOrGet(self, pks:list=None): # list of primary keys to filter with

        conditionList = [f"{key} = ?"
                        for key in pks]

        statement = f"""SELECT * FROM {self.__tablename__} 
                    WHERE 
                    {' AND '.join(conditionList)}"""

        values = [v for k, v in asdict(self).items() if k in pks]

        try:
            return self.save()
        except sqlite3.IntegrityError: # record already exists
            cursor = db.cursor()
            cursor.execute(statement, values)
            result = cursor.fetchone()
            db.commit()
            cursor.close()
            return self.instantiate(*result)

    @classmethod
    def delete(cls, conditions: dict= {}, logicalOperator: str = 'AND'):
        conditionList = []
        values = []
        
        for k,v in conditions.items():
            if isinstance(v,dict):
                operator = v.get('operator', '=')
                value = v.get('value')
            else:
                operator = '='
                value = v
                    
            conditionList.append(f"{k} {operator} ?")

            values.append(value)

        statement = f"""
        DELETE FROM {cls.__tablename__} 
        {'WHERE ' + f' {logicalOperator} '.join(conditionList) if len(conditionList) > 0 else ''}
        """

        db.execute(statement,values)
        db.commit()

        return True

    @classmethod
    def update(cls, conditions: dict= {}, logicalOperator: str = 'AND'):
        conditionList = []
        values = []
        newValues = []
        
        for k,v in conditions.items():
            if isinstance(v,dict):
                operator = v.get('operator', '=')
                value = v.get('value')
                newValue = v.get('newValue', value)
            else:
                operator = '='
                value = v
                newValue = v
                    
            conditionList.append(f"{k} {operator} ?")

            values.append(value)
            newValues.append(newValue)
        
        values = newValues + values

        statement = f"""
        UPDATE {cls.__tablename__}
        {'SET ' + ', '.join(conditionList) if len(conditionList) > 0 else ''}
        {'WHERE ' + f' {logicalOperator} '.join(conditionList) if len(conditionList) > 0 else ''}
        """
        
        cursor = db.cursor()
        cursor.execute(statement,values)
        db.commit()
        cursor.close()

        for key, value in conditions.items():
            conditions[key] = value.get("newValue", value.get("value"))

        return cls.filter(conditions) # return the affected rows

@dataclass
class TableWithId: # tables that have "id" field will inherit from this one in order to use the methods like getById

    @classmethod
    def getById(cls, id: int):
        return cls.filter({'id': id}, returns='one')