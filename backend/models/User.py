from dataclasses import dataclass
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

    def __init__(self):
        self.user = User(**db.execute("SELECT * FROM user WHERE ci=?", [self.ci]))
        return self.user

@dataclass
class Patient(CategorizedUser):
    __tablename__ = 'patient'
    
@dataclass # users from the medical personnel, those without further categorization (either doctor or medical assitant), will be stored only in this table and have limited permissions and access
class MedicalPersonnel(CategorizedUser):
    __tablename__ = 'medicalPersonnel'

@dataclass # users from the medical personnel, who are doctors. 
class Doctor(CategorizedUser):
    __tablename__ = 'doctor'

@dataclass # users from the medical personnel, who are medical assistants (i.e: nurses)
class MedicalAssitant(CategorizedUser):
    __tablename__ = 'medicalAssistant'

@dataclass
class Administrative(CategorizedUser):
    __tablename__ = 'administrative'