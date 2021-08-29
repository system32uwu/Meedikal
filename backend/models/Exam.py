from .User import Patient
from dataclasses import dataclass
from datetime import datetime
from .db import db, BaseModel

@dataclass
class Exam(BaseModel):
    id: int
    name: str
    preview: int

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), unique=True, nullable=False) 
    preview = db.Column(db.String()) 

@dataclass
class Parameter(BaseModel):
    id: int
    name: str
    measureUnit: str
    refMinValue: float
    refMaxValue: float

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), nullable=False) 
    measureUnit = db.Column(db.String()) 
    refMinValue = db.Column(db.Float)
    refMaxValue = db.Column(db.Float)

@dataclass
class Indication(BaseModel):
    id: int
    name: str
    description: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), nullable=False) 
    description = db.Column(db.String()) 

@dataclass
class ExHasPar(BaseModel):
    __tablename__ = 'exHasPar'

    idEx: int
    idPar: int

    idEx = db.Column(db.Integer, db.ForeignKey(Exam.id, ondelete='CASCADE'), primary_key=True)
    idPar = db.Column(db.Integer, db.ForeignKey(Parameter.id, ondelete='CASCADE'), primary_key=True)

@dataclass
class ExHasInd(BaseModel):
    __tablename__ = 'exHasInd'

    idEx: int
    idInd: int

    idEx = db.Column(db.Integer, db.ForeignKey(Exam.id, ondelete='CASCADE'), primary_key=True)
    idInd = db.Column(db.Integer, db.ForeignKey(Indication.id, ondelete='CASCADE'), primary_key=True)

@dataclass 
class TakesEx(BaseModel): # Patient < takesEx > Exam
    __tablename__ = 'takesEx'

    idExTaken: int
    idEx: int
    ciPa: int
    date: datetime
    results: object

    idExTaken = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idEx = db.Column(db.Integer, db.ForeignKey(Exam.id, ondelete='CASCADE'), primary_key=True)
    ciPa = db.Column(db.Integer, db.ForeignKey(Patient.ci, ondelete='CASCADE'), primary_key=True)
    date = db.Column(db.DateTime)
    results = db.Column(db.JSON)

@dataclass
class Laboratory(BaseModel):
    
    id: int
    name: str
    phoneNumber: str
    location: str
    email: str
    logo: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(64), unique=True, nullable=False) 
    phoneNumber = db.Column(db.VARCHAR(64), nullable=False) 
    location = db.Column(db.VARCHAR(64), nullable=False) 
    email = db.Column(db.VARCHAR(256), nullable=False) 
    logo = db.Column(db.String()) 

@dataclass
class HandlesEx(BaseModel): # [ takesEx ] < handlesEx > Laboratory
    __tablename__ = 'handlesEx'

    idEx: int
    idExTaken: int
    ciPa: int
    idLab: int

    idEx = db.Column(db.Integer, primary_key=True)
    idExTaken = db.Column(db.Integer, primary_key=True)
    ciPa = db.Column(db.Integer, primary_key=True)
    idLab = db.Column(db.Integer, db.ForeignKey(Laboratory.id, ondelete='CASCADE'))

    __table_args__ = (db.ForeignKeyConstraint([idEx,idExTaken,ciPa],[TakesEx.idEx,TakesEx.idExTaken,TakesEx.ciPa]),)
