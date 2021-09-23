from dataclasses import dataclass
from flask import json
from flask.wrappers import Request
from werkzeug.security import check_password_hash, generate_password_hash
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
    def filter(cls, conditions: dict= {}, logicalOperator:str = 'AND', returns='all'):

        try:
            userType = conditions['extraFilters']['userType']
            conditions.pop('extraFilters')
            conditions[f'{userType}.ci'] = {'value': 'user.ci', 'joins': True}
        finally:
            return super().filter(conditions,logicalOperator,returns)

    @classmethod
    def getRoles(cls, ci:int) -> list[str]:
        types = [User.__tablename__]

        if Administrative.filter({'ci': ci}, returns='one') is not None:
            types.append(Administrative.__tablename__)

        if Patient.filter({'ci': ci}, returns='one') is not None:
            types.append(Patient.__tablename__)
        
        if MedicalPersonnel.filter({'ci': ci}, returns='one') is not None:
            types.append(MedicalPersonnel.__tablename__)

            if Doctor.filter({'ci': ci}, returns='one') is not None:
                types.append(Doctor.__tablename__)
            
            if MedicalAssitant.filter({'ci': ci}, returns='one') is not None:
                types.append(MedicalAssitant.__tablename__)
                
        return types

    @classmethod
    def updatePassword(cls, ci, password) -> bool:
        password = generate_password_hash(password)
        
        statement = f"""UPDATE {cls.__tablename__} 
                        SET password = ? WHERE ci= ? """
        cursor = db.cursor()
        cursor.execute(statement, [password,ci])
        db.commit()

        return True if cursor.rowcount > 0 else False

class AuthUser:

    @classmethod
    def login(cls, ci:int, password:str): # returns True if the password is correct, if it's not, or the user doesn't exist, False
        user = User.getByCi(ci)
        try:
            if check_password_hash(user.password, password):
                now = datetime.utcnow() 
                payload = { # expires in 365 days.
                    'exp': now + timedelta(days=365),
                    'iat': now,
                    'sub': ci
                }
                token = jwt.encode(payload,Config.SECRET_KEY, algorithm="HS256")
                return token, user
            else:
                return None, None
        except: # self.user is None
            return None, None

    @staticmethod
    def verifyToken(token) -> int: # exceptions handled by auth error handler.
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

@dataclass
class Patient(BaseModel):
    __tablename__ = 'patient'
    ci: int
    
@dataclass # users from the medical personnel, those without further categorization (either doctor or medical assitant), will be stored only in this table and have limited permissions and access
class MedicalPersonnel(BaseModel):
    __tablename__ = 'medicalPersonnel'
    ci: int
    
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
class Doctor(BaseModel):
    __tablename__ = 'doctor'
    ci: int
    
@dataclass # users from the medical personnel, who are medical assistants (i.e: nurses)
class MedicalAssitant(BaseModel):
    __tablename__ = 'medicalAssistant'
    ci: int

@dataclass
class Administrative(BaseModel):
    __tablename__ = 'administrative'
    ci: int