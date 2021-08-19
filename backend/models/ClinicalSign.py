from .Appointment import Appointment
from .User import Patient
from dataclasses import dataclass
from . import db

@dataclass
class ClinicalSign(db.Model):
    __tablename__ = 'clinicalSign'

    id: int
    name: str
    description: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), unique=True, nullable=False) 
    description = db.Column(db.VARCHAR(512)) 

@dataclass
class registersCs(db.Model): # { Patient < attendsTo > [ Doctor < assignedTo > Appointment] } < registersCs > ClinicalSign
    __tablename__ = 'registersCs'

    idAp: int
    ciPa: int
    idCs: int
    detail: str

    idAp = db.Column(db.Integer, db.ForeignKey(Appointment.id, ondelete='CASCADE'), primary_key=True)
    ciPa = db.Column(db.Integer, db.ForeignKey(Patient.ci, ondelete='CASCADE'), primary_key=True)
    idCs = db.Column(db.Integer, db.ForeignKey(ClinicalSign.id, ondelete='CASCADE'), primary_key=True)
    detail = db.Column(db.VARCHAR(256))