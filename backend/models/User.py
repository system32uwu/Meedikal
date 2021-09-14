from dataclasses import dataclass
from flask import json
from flask.wrappers import Request
from werkzeug.security import check_password_hash
from .db import BaseModel, db
from datetime import datetime, timedelta
from typing import Optional
from config import Config
import jwt

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

            if k != 'password':
                values.append(value)

            newValues.append(newValue)
        
        try:
            # can't compare hashes (even if it's the same password) since they will always be different.
            oldConditionList = conditionList.copy()
            oldConditionList.remove("password = ?")
        except ValueError:
            pass
        
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
            conditions = None
            userType = None
        
        if userType is None:
            return cls.filter(conditions,logicalOperator,returns)

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

class AuthUser:
    ci:int = None
    password:str = None
    user:User = None
    token:str = None

    def __init__(self, ci:int,password:str, token:str=None):
        self.ci = ci
        self.password = password
        self.token = token

    def login(self) -> bool: # returns True if the password is correct, if it's not, or the user doesn't exist, False
        self.user = User.getByCi(self.ci)
        try:
            return check_password_hash(self.user.password, self.password)
        except: # self.user is None
            return False

    def issueAuthToken(self):
        now = datetime.utcnow() 
        payload = { # expires in 365 days.
            'exp': now + timedelta(days=365),
            'iat': now,
            'sub': self.ci
        }
        _jwt = jwt.encode(payload,Config.SECRET_KEY, algorithm="HS256")
        self.token = _jwt
        return self.token

    @staticmethod
    def verifyToken(token): # exceptions handled by auth error handler.
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return payload['sub']

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
    def getBySpecialty(cls, returns:str='all', request:Request=None, title:str=None):
        userType = 'medicalPersonnel'
        
        if title is None:
            try:
                conditions = json.loads(request.data)
                title = conditions['title']
                userType = conditions['extraFilters']['userType']
            except:
                userType = 'medicalPersonnel'

        statement = f"""
                SELECT user.* 
                FROM {userType}, user, mpHasSpec, specialty
                WHERE {userType}.ci = mpHasSpec.ciMp
                AND {userType}.ci == {User.__tablename__}.ci
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