from dataclasses import asdict, dataclass
from flask import json
from flask.wrappers import Request
from werkzeug.security import check_password_hash
from .db import BaseModel, db
from datetime import datetime
from typing import Optional

class SharedUserMethods(BaseModel):

    @classmethod
    def getByCi(cls, ci: int):
        return cls.filter({'ci': ci}, returns='one')

@dataclass
class User(SharedUserMethods):
    __tablename__ = 'user'
    
    ci: int
    name1: str
    surname1: str
    sex: str
    birthdate: datetime
    location: str
    email: str
    password: str
    name2: Optional[str] = None
    surname2: Optional[str] = None
    genre: Optional[str] = None
    active: Optional[bool] = True

    @classmethod
    def update(cls, conditions: dict= {}, logicalOperator: str = 'AND'):
        try:
            conditionList = [f"{key} {value.get('operator', '=')} ?"
                            for key, value in conditions.items()]
        except:
            conditionList = [f"{key} = ?"
                            for key in conditions.keys()]
        
        # can't compare hashes (even if it's the same password) since they will always be different.
        oldConditionList = conditionList.copy()
        oldConditionList.remove("password = ?")

        values = [v.get('value', v)
                 for k, v in conditions.items() 
                 if k != 'password'] 

        newValues = [v.get('newValue', v.get('value', v)) 
                    for v in conditions.values()]
        
        values = newValues + values

        statement = f"""
        UPDATE {cls.__tablename__}
        {'SET ' + ', '.join(conditionList) if len(conditionList) > 0 else ''}
        {'WHERE ' + f' {logicalOperator} '.join(oldConditionList) if len(oldConditionList) > 0 else ''}
        """

        cursor = db.cursor()
        cursor.execute(statement,values)
        db.commit()
        cursor.close()

        for key, value in conditions.items():
            conditions[key] = value.get("newValue", value.get("value"))

        return cls.filter(conditions) # return the affected rows

    @classmethod # dict shape: {'key': 'value'} || {'key': {'value': 'v', 'operator': '='}}
    def getByType(cls, logicalOperator: str = 'AND', returns:str='all', request:Request=None):
        
        try:
            conditions = json.loads(request.data)
            userType = conditions.get('extraFilters', {}).get('userType', None)
            conditions.pop('extraFilters')
        except:
            userType = None
        
        if userType is None:
            return cls.filter(conditions,logicalOperator,returns)

        try:
            conditionList = [f"{key} {value.get('operator', '=')} ?"
                        for key, value in conditions.items()]

            values = [v.get('value', None) for v in conditions.values() 
                    if v is not None]
        except:
            conditionList = [f"{key} = ?" for key in conditions.keys()]

            values = [v for v in conditions.values()]

        statement = f"""
        SELECT {User.__tablename__}.* FROM {User.__tablename__}, {userType} 
        {'WHERE ' + f'{User.__tablename__}.ci = {userType}.ci '}
        {logicalOperator if len(conditionList) > 0 else ''}
        {f' {logicalOperator} '.join(conditionList) if len(conditionList) > 0 else ''}
        """

        if returns == 'all':
            return [cls(*obj) for obj in db.execute(statement, values).fetchall()]
        else:
            try:
                return cls(*db.execute(statement, values).fetchone())
            except:
                return None

    def check_password(self, password) -> bool:
        return check_password_hash(self.password, password)

@dataclass # since phone is a multivalued attribute, it has its own table.
class UserPhone(BaseModel):
    __tablename__ = 'userPhone'

    ci: int
    phone: str # since phone numbers aren't real numbers it's better to store them as strings. Some countries (like Uruguay), start their cellphone numbers with a 0, which on input would be ignored by the DBMS if the datatype was Integer. 

    @classmethod
    def getByCi(cls, ci: int):
        return cls.filter({'ci': ci}, returns='all')

class CategorizedUser(SharedUserMethods):
    ci: int
    user: User = None

    def __init__(self, ci:int):
        self.ci = ci
        self.user = self.getByCi(ci)
        return self.user

@dataclass
class Patient(CategorizedUser):
    __tablename__ = 'patient'
    ci: int

    def __init__(self, ci: int):
        super().__init__(ci)
    
@dataclass # users from the medical personnel, those without further categorization (either doctor or medical assitant), will be stored only in this table and have limited permissions and access
class MedicalPersonnel(CategorizedUser):
    __tablename__ = 'medicalPersonnel'
    ci: int
    
    def __init__(self, ci: int):
        super().__init__(ci)

    @classmethod
    def getBySpecialty(cls, returns:str='all', request:Request=None):
        conditions = json.loads(request.data)
        title = conditions['title']

        try:
            userType = conditions.get('extraFilters', {}).get('userType', None)
        except:
            userType = 'medicalPersonnel'

        statement = f"""
                SELECT user.* 
                FROM {userType}, user, mpHasSpec, specialty
                WHERE {userType}.ci = mpHasSpec.ciMp
                AND {userType}.ci == {User.__tablename__}.ci'
                AND specialty.title = ?
                AND mpHasSpec.idSpec = specialty.id
                """

        if returns == 'all':
            return [User(*obj) for obj in db.execute(statement, [title]).fetchall()]
        else:
            try:
                return User(*db.execute(statement, [title]).fetchone())
            except:
                return None

@dataclass # users from the medical personnel, who are doctors. 
class Doctor(CategorizedUser):
    __tablename__ = 'doctor'
    ci: int
    
    def __init__(self, ci: int):
        super().__init__(ci)
@dataclass # users from the medical personnel, who are medical assistants (i.e: nurses)
class MedicalAssitant(CategorizedUser):
    __tablename__ = 'medicalAssistant'
    ci: int

    def __init__(self, ci: int):
        super().__init__(ci)

@dataclass
class Administrative(CategorizedUser):
    __tablename__ = 'administrative'
    ci: int
    
    def __init__(self, ci: int):
        super().__init__(ci)