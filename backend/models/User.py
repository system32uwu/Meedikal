from dataclasses import dataclass
from werkzeug.security import check_password_hash
from . import db
from datetime import datetime

@dataclass # base user class
class User(db.Model):

    CI: int
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

    CI = db.Column(db.Integer, primary_key=True)
    name1 = db.Column(db.VARCHAR(32), nullable=False)
    name2 = db.Column(db.VARCHAR(32))
    surname1 = db.Column(db.VARCHAR(32), nullable=False)
    surname2 = db.Column(db.VARCHAR(32))
    sex = db.Column(db.CHAR(1), default='M', nullable=False)
    genre = db.Column(db.VARCHAR(32), default='Male')
    birthdate = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.VARCHAR(256))
    email = db.Column(db.VARCHAR(256))
    active = db.Column(db.BOOLEAN, default=True, nullable=False)
    password = db.Column(db.VARCHAR(128), nullable=False)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password, password)

@dataclass # since phone is a multivalued attribute, it has its own table.
class UserPhone(db.Model):

    CI: int
    phone: str # since phone numbers aren't real numbers it's better to store them as strings. Some countries (like Uruguay), start their cellphone numbers with a 0, which on input would be ignored by the DBMS if the datatype was Integer. 

    __tablename__ = 'userPhone'
    CI = db.Column(db.Integer, db.ForeignKey(User.CI, ondelete='CASCADE'), primary_key=True)
    phone = db.Column(db.VARCHAR(32), primary_key=True) # some countries' phone numbers are quite long 

@dataclass
class Patient(db.Model):

    CI: int

    CI = db.Column(db.Integer, db.ForeignKey(User.CI, ondelete='CASCADE'), primary_key=True)
    
@dataclass # users from the medical personnel, those without further categorization (either doctor or medical assitant), will be stored only in this table and have limited permissions and access
class MedicalPersonnel(db.Model):

    CI: int

    __tablename__ = 'medicalPersonnel'
    CI = db.Column(db.Integer, db.ForeignKey(User.CI, ondelete='CASCADE'), primary_key=True)

@dataclass # users from the medical personnel, who are doctors.
class Doctor(db.Model):

    CI: int

    CI = db.Column(db.Integer, db.ForeignKey(MedicalPersonnel.CI, ondelete='CASCADE'), primary_key=True)

@dataclass # users from the medical personnel, who are medical assistants (i.e: nurses)
class MedicalAssitant(db.Model):

    CI: int

    __tablename__ = 'medicalAssistant'
    CI = db.Column(db.Integer, db.ForeignKey(MedicalPersonnel.CI, ondelete='CASCADE'), primary_key=True)

@dataclass
class Administrative(db.Model):

    CI: int

    CI = db.Column(db.Integer, db.ForeignKey(User.CI, ondelete='CASCADE'), primary_key=True)
