from .ClinicalSign import ClinicalSign
from .Appointment import Appointment, AttendsTo
from dataclasses import dataclass
from datetime import datetime
from .db import db, BaseModel
from .User import User

@dataclass
class Disease(BaseModel):
    id: int
    name: str
    description: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), unique=True, nullable=False) 
    description = db.Column(db.VARCHAR(512)) 

@dataclass
class Category(BaseModel):
    id: int
    name: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), unique=True, nullable=False) 

@dataclass
class DiseaseCat(BaseModel): # Disease <diseaseCat> Category
    __tablename__ = 'diseaseCat'

    idDisease: int
    idCat: int

    idDisease = db.Column(db.Integer, db.ForeignKey(Disease.id, ondelete='CASCADE'), primary_key=True)
    idCat = db.Column(db.Integer, db.ForeignKey(Category.id, ondelete='CASCADE'), primary_key=True) 

@dataclass
class USufferedFrom(BaseModel): # User < uSufferedFrom > Disease
    __tablename__ = 'uSufferedFrom'

    ciUser: int
    idDisease: int
    fromDate: datetime
    toDate: datetime
    notes: str

    ciUser = db.Column(db.Integer, db.ForeignKey(User.ci, ondelete='CASCADE'), primary_key=True)
    idDisease = db.Column(db.Integer, db.ForeignKey(Disease.id, ondelete='CASCADE'), primary_key=True)
    fromDate = db.Column(db.DateTime, primary_key=True, nullable=False)
    toDate = db.Column(db.DateTime)
    notes = db.Column(db.VARCHAR(128)) 


@dataclass
class Diagnoses(BaseModel): # { Patient < attendsTo > [ Doctor < assignedTo > Appointment] } < diagnoses > Disease

    idAp: int
    ciPa: int
    idDis: int
    detail: str

    idAp = db.Column(db.Integer, primary_key=True)
    ciPa = db.Column(db.Integer, primary_key=True)
    idDis = db.Column(db.Integer, db.ForeignKey(Disease.id, ondelete='CASCADE'), primary_key=True)
    detail = db.Column(db.VARCHAR(256))

    __table_args__ = (db.ForeignKeyConstraint([idAp,ciPa], [AttendsTo.idAp,AttendsTo.ciPa], ondelete='CASCADE'),)
