from datetime import datetime
from .User import MedicalPersonnel, Patient
from dataclasses import dataclass
from . import db

@dataclass
class Treatment(db.Model):
    
    id: int
    name: str
    preview: str
    indications: object
    avgSessionTime: int # in seconds

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), unique=True, nullable=False) 
    preview = db.Column(db.String())
    indications = db.Column(db.JSON)
    avgSessionTime = db.Column(db.Integer)

@dataclass
class Follows(db.Model): # Patient < follows > Treatment
    idFollows: int
    idTreatment: int
    ciPa: int
    beginDate: datetime
    endDate: datetime
    schedule: object
    result: str

    idFollows = db.Column(db.Integer, primary_key=True)
    ciPa = db.Column(db.Integer, db.ForeignKey(Patient.ci, ondelete='CASCADE'), primary_key=True)
    idTreatment = db.Column(db.Integer, db.ForeignKey(Treatment.id, ondelete='CASCADE'), primary_key=True)
    beginDate = db.Column(db.DateTime)
    endDate = db.Column(db.DateTime)
    schedule = db.Column(db.JSON)
    result = db.Column(db.VARCHAR(64))

@dataclass
class TakesCare(db.Model): # MedicalPersonnel < takesCare > [ Patient < follows > Treatment ] 
    __tablename__ = 'takesCare'
    idFollows: int
    idTreatment: int
    ciPa: int
    ciMp: int
    date: datetime

    idFollows = db.Column(db.Integer, primary_key=True)
    idTreatment = db.Column(db.Integer, primary_key=True)
    ciPa = db.Column(db.Integer, primary_key=True)
    ciMp = db.Column(db.Integer, db.ForeignKey(MedicalPersonnel.ci, ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    date = db.Column(db.DateTime, primary_key=True)

    __table_args__ = (db.ForeignKeyConstraint([idFollows,idTreatment, ciPa], [Follows.idFollows,Follows.idTreatment, Follows.ciPa], ondelete='CASCADE'),)
