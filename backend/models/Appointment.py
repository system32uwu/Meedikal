from .User import Patient, Doctor
from dataclasses import dataclass
from . import db
from datetime import datetime, date, time
from sqlalchemy import Enum

appointmentStates = ('OK','CANCELLED', 'RESCHEDULING')
appointmentStatesEnum = Enum(*appointmentStates, name='appointmentState')

@dataclass
class Appointment(db.Model):

    ID: int
    name: str
    date: date
    state: Enum
    timeBegins: time
    timeEnds: time
    ETPP: int # estimated time per patient, in seconds
    maxTurns: int # max patients to be attended

    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), nullable=False) 
    date = db.Column(db.Date, nullable=False)
    state = db.Column(appointmentStatesEnum, nullable=False)
    timeBegins = db.Column(db.Time)
    timeEnds = db.Column(db.Time)
    ETPP = db.Column(db.Integer, default=720) # 12 minutes default
    maxTurns = db.Column(db.Integer, default=1)

@dataclass
class Symptom(db.Model):
    
    ID: int
    name: str
    description: str

    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), nullable=False) 
    description = db.Column(db.VARCHAR(512)) 

@dataclass
class ClinicalSign(db.Model):
    __tablename__ = 'clinicalSign'

    ID: int
    name: str
    description: str

    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), unique=True, nullable=False) 
    description = db.Column(db.VARCHAR(512)) 

@dataclass
class AssignedTo(db.Model): # Doctor < assignedTo > Appointment
    __tablename__ = 'assignedTo'

    IDAp: int
    CIDoc: int

    IDAp = db.Column(db.Integer, db.ForeignKey(Appointment.ID, ondelete='CASCADE'), primary_key=True)
    CIDoc = db.Column(db.Integer, db.ForeignKey(Doctor.CI, ondelete='CASCADE'))

@dataclass
class AttendsTo(db.Model): # Patient < attendsTo > [ Doctor < assignedTo > Appointment]
    __tablename__ = 'attendsTo'

    IDAp: int
    CIPa: int
    motive: str
    number: int
    time: time

    IDAp = db.Column(db.Integer, db.ForeignKey(Appointment.ID, ondelete='CASCADE'), primary_key=True)
    CIPa = db.Column(db.Integer, db.ForeignKey(Patient.CI, ondelete='CASCADE'), primary_key=True)
    motive = db.Column(db.VARCHAR(256))
    number = db.Column(db.Integer)
    time = db.Column(db.Time)