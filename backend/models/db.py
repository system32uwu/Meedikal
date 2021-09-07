from dataclasses import asdict, dataclass
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
            return db.execute(statement, values).fetchall()
        else:
            return db.execute(statement, values).fetchone()

    def save(self, fetchBeforeReturn=False):
        attrs = asdict(self).keys()
        values = [v for v in asdict(self).values()]
        
        statement = f"""
        INSERT INTO {self.__tablename__} ({','.join(attrs)})
        VALUES ({",".join("?"*len(values))})
        """
        try:
            db.cursor().execute(statement, values)
            db.commit()
            if fetchBeforeReturn:
                print(f'lastrowid: {db.cursor().lastrowid}')
            return self, True
        except Exception as exc:
            print(f'exc: {exc}')
            db.rollback()
            return self, False

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