from .ClinicalSign import ClinicalSign
from .Appointment import Appointment
from dataclasses import dataclass
from datetime import datetime
from . import db
from .User import Patient, User

@dataclass
class Disease(db.Model):
    id: int
    name: str
    description: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), unique=True, nullable=False) 
    description = db.Column(db.VARCHAR(512)) 

@dataclass
class Category(db.Model):
    id: int
    name: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), unique=True, nullable=False) 

@dataclass
class DiseaseCat(db.Model): # Disease <diseaseCat> Category
    __tablename__ = 'diseaseCat'

    idDisease: int
    idCat: int

    idDisease = db.Column(db.Integer, db.ForeignKey(Disease.id, ondelete='CASCADE'), primary_key=True)
    idCat = db.Column(db.Integer, db.ForeignKey(Category.id, ondelete='CASCADE'), primary_key=True) 

@dataclass
class USufferedFrom(db.Model): # User < uSufferedFrom > Disease
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
class Diagnoses(db.Model): # { Patient < attendsTo > [ Doctor < assignedTo > Appointment] } < diagnoses > Disease

    idAp: int
    ciPa: int
    idDis: int
    detail: str

    idAp = db.Column(db.Integer, db.ForeignKey(Appointment.id, ondelete='CASCADE'), primary_key=True)
    ciPa = db.Column(db.Integer, db.ForeignKey(Patient.ci, ondelete='CASCADE'), primary_key=True)
    idDis = db.Column(db.Integer, db.ForeignKey(ClinicalSign.id, ondelete='CASCADE'), primary_key=True)
    detail = db.Column(db.VARCHAR(256))