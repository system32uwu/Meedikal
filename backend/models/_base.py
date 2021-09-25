from dataclasses import dataclass, fields
import sqlite3

from util.createDb import getDb

db = getDb()

def buildQueryComponents(cls:'BaseModel', conditions:dict={}, logicalOperator:str='AND', command:str='SELECT', returns='tuple'):
    extraTables = []
    conditionList = []
    values = []
    newValues = []

    if command == 'INSERT':
        data = {}

        for f in fields(cls):
            data[f.name] = conditions.get(f.name)
        conditions = [k for k in data.keys()]
        values = [v for v in data.values()]

    else: # filter
        if conditions is not None:
            for k,v in conditions.items():
                if '.' in str(k): # table.attribute
                    table = str(k).split(".")[0]
                    if table not in extraTables and table != cls.__tablename__:
                        extraTables.append(table)
                else:
                    if command != 'UPDATE':
                        k = f'{cls.__tablename__}.{str(k)}'

                if isinstance(v,dict):
                    operator = v.get('operator', '=')
                    value = v.get('value')
                    
                    if command == 'UPDATE':
                        newValue = v.get('newValue', value)
                        newValues.append(newValue)

                    joinsTable = v.get('joins', False)
                else:
                    operator = '='
                    value = v
                    if command == 'UPDATE':
                        newValues.append(v)

                    joinsTable = False

                if value is None:
                    operator = 'IS'

                if not joinsTable:
                    conditionList.append(f"{k} {operator} ?")
                    values.append(value)
                else:
                    conditionList.append(f"{k} {operator} {value}")
                    table = str(value).split(".")[0] #table.attribute
                    if table not in extraTables and table != cls.__tablename__:
                        extraTables.append(table)
    
    statement = command

    if command == 'UPDATE':
        values = newValues + values
        statement += f' {cls.__tablename__}'

    if command == 'SELECT':
        statement += f' {cls.__tablename__}.*'
    
    if command == 'SELECT' or command == 'DELETE':
        
        statement += f'\nFROM {cls.__tablename__}'
        statement += "," if len(extraTables) > 0 else ''
        statement += ', '.join(extraTables)

    elif command == 'INSERT':
        statement += '\nINTO '
        statement += f'''\n{cls.__tablename__} 
                    ({",".join(conditions)}) 
                    VALUES({",".join("?"*len(values))})'''

    elif command == 'UPDATE':
        statement += '\nSET ' if len(conditionList) > 0 else ''
        statement += ', '.join(conditionList).replace("IS","=")

    if command != 'INSERT':
        statement += '\nWHERE ' + f' {logicalOperator} '.join(conditionList) if len(conditionList) > 0 else ''

    if returns == 'tuple':
        return extraTables, conditionList, values, statement
    
    if command == 'SELECT':
        result = db.execute(statement, values)
        if returns == 'all':
            return [cls(*data) for data in result.fetchall()]
        else:
            try:
                return cls(*result.fetchone())
            except:
                return None
    else:
        cursor = db.cursor()
        cursor.execute(statement, values)
        db.commit()
        
        if command == 'DELETE' or command == 'UPDATE':
            return cursor.rowcount
            
        elif command == 'INSERT':
            lastrowid = cursor.lastrowid
                
            for key, value in data.items():
                if key == 'id':
                    value = lastrowid
                data[key] = value
            conditions = data

        if cursor.rowcount > 0:
            return cls.filter(conditions, returns=returns)
        else:
            if returns == 'all':
                return []
            else:
                return None

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
    def filter(cls, conditions: dict= {}, logicalOperator:str = 'AND', returns='all'):
        return buildQueryComponents(cls, conditions, logicalOperator, 'SELECT', returns)

    @classmethod
    def save(cls, conditions: dict= {}, returns='one') -> 'BaseModel':
        return buildQueryComponents(cls, conditions, command='INSERT', returns=returns)

    @classmethod 
    def saveOrGet(cls, conditions: dict= {}, logicalOperator:str = 'AND', returns='all'):
        try:
            return cls.save(conditions, returns)
        except sqlite3.IntegrityError: # record already exists
            return cls.filter(conditions,logicalOperator,returns)

    @classmethod
    def delete(cls, conditions: dict= {}, logicalOperator: str = 'AND', returns='DELETE'):
        return buildQueryComponents(cls, conditions, logicalOperator, 'DELETE', returns)

    @classmethod
    def update(cls, conditions: dict= {}, logicalOperator: str = 'AND', returns='all'):
        return buildQueryComponents(cls, conditions, logicalOperator, 'UPDATE', returns)

@dataclass
class TableWithId: # tables that have "id" field will inherit from this one in order to use the methods like getById

    @classmethod
    def getById(cls: BaseModel, id: int):
        return cls.filter({'id': id}, returns='one')