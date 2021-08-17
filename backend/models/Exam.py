from dataclasses import dataclass
from . import db

@dataclass
class Exam(db.Model):
    ID: int
    name: str
    preview: int

    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), unique=True, nullable=False) 
    preview = db.Column(db.String()) 

@dataclass
class Parameter(db.Model):
    ID: int
    name: str
    measureUnit: str
    refMinValue: float
    refMaxValue: float

    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), nullable=False) 
    measureUnit = db.Column(db.String()) 
    refMinValue = db.Column(db.Float)
    refMaxValue = db.Column(db.Float)

@dataclass
class Indication(db.Model):
    ID: int
    name: str
    description: str

    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), nullable=False) 
    description = db.Column(db.String()) 

class Laboratory(db.Model):
    
    ID: int
    name: str
    phoneNumber: str
    location: str
    email: str
    logo: str

    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(64), unique=True, nullable=False) 
    phoneNumber = db.Column(db.VARCHAR(64), nullable=False) 
    location = db.Column(db.VARCHAR(64), nullable=False) 
    email = db.Column(db.VARCHAR(256), nullable=False) 
    logo = db.Column(db.String()) 


class ExHasPar(db.Model):
    __tablename__ = 'exHasPar'

    IDEx: int
    IDPar: int

    IDEx = db.Column(db.Integer, db.ForeignKey(Exam.ID, ondelete='CASCADE'), primary_key=True)
    IDPar = db.Column(db.Integer, db.ForeignKey(Parameter.ID, ondelete='CASCADE'), primary_key=True)

class ExHasInd(db.Model):
    __tablename__ = 'exHasInd'

    IDEx: int
    IDInd: int

    IDEx = db.Column(db.Integer, db.ForeignKey(Exam.ID, ondelete='CASCADE'), primary_key=True)
    IDInd = db.Column(db.Integer, db.ForeignKey(Indication.ID, ondelete='CASCADE'), primary_key=True)

# class handlesEx(db.Model):
#     __tablename__ = 'handlesEx'

#     IDEx: int
#     IDInd: int

#     IDEx = db.Column(db.Integer, db.ForeignKey(Exam.ID, ondelete='CASCADE'), primary_key=True)
#     IDLab = db.Column(db.Integer, db.ForeignKey(Laboratory.ID, ondelete='CASCADE'), primary_key=True)
    