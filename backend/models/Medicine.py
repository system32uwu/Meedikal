from datetime import datetime
from .User import Doctor, Patient
from dataclasses import dataclass
from .db import db, BaseModel

@dataclass
class Medicine(BaseModel):
    id: int
    name: str
    description: str
    notes: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), unique=True, nullable=False) 
    description = db.Column(db.String())
    notes = db.Column(db.String())

@dataclass
class Manufacturer(BaseModel):

    id: int
    name: str
    location: str
    email: str
    phoneNumber: str
    logo: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), unique=True, nullable=False)
    location = db.Column(db.VARCHAR(256))
    email = db.Column(db.VARCHAR(256))
    phoneNumber = db.Column(db.VARCHAR(32))
    logo = db.Column(db.String())

@dataclass 
class ManufacturedBy(BaseModel):
    __tablename__ = 'manufacturedBy'

    idMed: int
    idManufacturer: int

    idMed = db.Column(db.Integer, db.ForeignKey(Medicine.id, ondelete='CASCADE'), primary_key=True)
    idManufacturer = db.Column(db.Integer, db.ForeignKey(Manufacturer.id, ondelete='CASCADE'), primary_key=True)
    
@dataclass 
class TakesMed(BaseModel):
    __tablename__ = 'takesMed'

    idMed: int
    ciPa: int
    detail: str

    idMed = db.Column(db.Integer, db.ForeignKey(Medicine.id, ondelete='CASCADE'), primary_key=True)
    ciPa = db.Column(db.Integer, db.ForeignKey(Patient.ci, ondelete='CASCADE'), primary_key=True)
    detail = db.Column(db.VARCHAR(256))
    

@dataclass 
class Prescribes(BaseModel): # Doctor < prescribes > [ Patient < takesMed > Medicine ]

    idMed: int
    ciPa: int
    ciDoc: int
    date: datetime

    idMed = db.Column(db.Integer, primary_key=True)
    ciPa = db.Column(db.Integer, primary_key=True)
    ciDoc = db.Column(db.Integer, db.ForeignKey(Doctor.ci, ondelete='CASCADE'), primary_key=True)
    date = db.Column(db.DateTime, primary_key=True)

    __table_args__ = (db.ForeignKeyConstraint([idMed,ciPa], [TakesMed.idMed,TakesMed.ciPa], ondelete='CASCADE'),)