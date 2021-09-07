from dataclasses import dataclass
from werkzeug.security import check_password_hash
from .db import db
from datetime import datetime
from typing import Optional

@dataclass
class User:
    __tablename__ = 'user'
    
    ci: int
    name1: str
    name2: Optional[str]
    surname1: str
    surname2: Optional[str]
    sex: str
    genre: Optional[str]
    birthdate: datetime
    location: str
    email: str
    password: str
    active: Optional[bool] = True

    @classmethod
    def getByCi(cls, ci:int):
        return User(*db.execute(f"SELECT * FROM {cls.__tablename__} WHERE ci=?", [ci]).fetchone())

    def check_password(self, password) -> bool:
        return check_password_hash(self.password, password)

@dataclass # since phone is a multivalued attribute, it has its own table.
class UserPhone:
    __tablename__ = 'userPhone'

    ci: int
    phone: str # since phone numbers aren't real numbers it's better to store them as strings. Some countries (like Uruguay), start their cellphone numbers with a 0, which on input would be ignored by the DBMS if the datatype was Integer. 

@dataclass
class Patient:
    __tablename__ = 'patient'

    ci: int
    
@dataclass # users from the medical personnel, those without further categorization (either doctor or medical assitant), will be stored only in this table and have limited permissions and access
class MedicalPersonnel:
    __tablename__ = 'medicalPersonnel'

    ci: int

@dataclass # users from the medical personnel, who are doctors. 
class Doctor:
    __tablename__ = 'doctor'

    ci: int

@dataclass # users from the medical personnel, who are medical assistants (i.e: nurses)
class MedicalAssitant:
    __tablename__ = 'medicalAssistant'

    ci: int

@dataclass
class Administrative:

    ci: int

@dataclass
class UIsRelatedTo: # User1 < uIsRelatedTo > User2
    __tablename__ = 'uIsRelatedTo'
    
    _id:int
    user1: int
    user2: int
    relationType: Optional[str] # user1 is father of user2