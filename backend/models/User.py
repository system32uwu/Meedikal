from dataclasses import dataclass
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash
from .db import BaseModel, db
from datetime import datetime

@dataclass # base user class
class User(BaseModel):

    ci: int
    name1: str
    name2: str
    surname1: str
    surname2: str
    sex: str
    genre: str
    birthdate: datetime
    location: str
    email: str
    active: bool
    password: str

    ci = db.Column(db.Integer, primary_key=True)
    name1 = db.Column(db.VARCHAR(32), nullable=False)
    name2 = db.Column(db.VARCHAR(32))
    surname1 = db.Column(db.VARCHAR(32), nullable=False)
    surname2 = db.Column(db.VARCHAR(32))
    sex = db.Column(db.CHAR(1), default='M', nullable=False)
    genre = db.Column(db.VARCHAR(32), default='Male')
    birthdate = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.VARCHAR(256))
    email = db.Column(db.VARCHAR(256))
    active = db.Column(db.BOOLEAN, nullable=False)
    password = db.Column(db.VARCHAR(128), nullable=False)

    phoneNumbers = relationship('UserPhone', back_populates='users')

    def check_password(self, password) -> bool:
        return check_password_hash(self.password, password)

@dataclass # since phone is a multivalued attribute, it has its own table.
class UserPhone(BaseModel):
    __tablename__ = 'userPhone'

    ci: int
    phone: str # since phone numbers aren't real numbers it's better to store them as strings. Some countries (like Uruguay), start their cellphone numbers with a 0, which on input would be ignored by the DBMS if the datatype was Integer. 

    ci = db.Column(db.Integer, db.ForeignKey(User.ci, ondelete='CASCADE'), primary_key=True)
    phone = db.Column(db.VARCHAR(32), primary_key=True) # some countries' phone numbers are quite long 

    users = relationship('User', back_populates='phoneNumbers')

@dataclass
class Patient(BaseModel):

    ci: int

    ci = db.Column(db.Integer, db.ForeignKey(User.ci, ondelete='CASCADE'), primary_key=True)

    base: User = relationship('User') # in order to get the base attributes
    
@dataclass # users from the medical personnel, those without further categorization (either doctor or medical assitant), will be stored only in this table and have limited permissions and access
class MedicalPersonnel(BaseModel):
    __tablename__ = 'medicalPersonnel'

    ci: int

    ci = db.Column(db.Integer, db.ForeignKey(User.ci, ondelete='CASCADE'), primary_key=True)

    base: User = relationship('User') # in order to get the base attributes

@dataclass # users from the medical personnel, who are doctors. 
class Doctor(BaseModel):

    ci: int

    ci = db.Column(db.Integer, db.ForeignKey(MedicalPersonnel.ci, ondelete='CASCADE'), primary_key=True)

    base = relationship('MedicalPersonnel') # in order to get the base attributes

@dataclass # users from the medical personnel, who are medical assistants (i.e: nurses)
class MedicalAssitant(BaseModel):
    __tablename__ = 'medicalAssistant'

    ci: int

    ci = db.Column(db.Integer, db.ForeignKey(MedicalPersonnel.ci, ondelete='CASCADE'), primary_key=True)

    base = relationship('MedicalPersonnel') # in order to get the base attributes

@dataclass
class Administrative(BaseModel):

    ci: int

    ci = db.Column(db.Integer, db.ForeignKey(User.ci, ondelete='CASCADE'), primary_key=True)

    base: User = relationship('User') # in order to get the base attributes

@dataclass
class UIsRelatedTo(BaseModel): # User1 < uIsRelatedTo > User2
    __tablename__ = 'uIsRelatedTo'
    
    user1: int
    user2: int
    typeUser1: str # son
    typeUser2: str # father

    user1 = db.Column(db.Integer, db.ForeignKey(User.ci, ondelete='CASCADE'), primary_key=True)
    user2 = db.Column(db.Integer, db.ForeignKey(User.ci, ondelete='CASCADE'), primary_key=True)
    typeUser1 = db.Column(db.VARCHAR(32))
    typeUser2 = db.Column(db.VARCHAR(32))