from .User import MedicalAssitant, Patient, Doctor
from dataclasses import dataclass
from . import db
from datetime import datetime, date, time
from sqlalchemy import Enum

appointmentStates = ('OK','CANCELLED', 'RESCHEDULING')
appointmentStatesEnum = Enum(*appointmentStates, name='appointmentState')

@dataclass
class Appointment(db.Model):

    id: int
    name: str
    date: date
    state: Enum
    timeBegins: time
    timeEnds: time
    etpp: int # estimated time per patient, in seconds
    maxTurns: int # max patients to be attended

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), nullable=False) 
    date = db.Column(db.Date, nullable=False)
    state = db.Column(appointmentStatesEnum, nullable=False)
    timeBegins = db.Column(db.Time)
    timeEnds = db.Column(db.Time)
    etpp = db.Column(db.Integer, default=720) # 12 minutes default
    maxTurns = db.Column(db.Integer, default=1)

@dataclass
class AssignedTo(db.Model): # Doctor < assignedTo > Appointment
    __tablename__ = 'assignedTo'

    idAp: int
    ciDoc: int

    idAp = db.Column(db.Integer, db.ForeignKey(Appointment.id, ondelete='CASCADE'), primary_key=True)
    ciDoc = db.Column(db.Integer, db.ForeignKey(Doctor.ci, ondelete='CASCADE'))

@dataclass
class AssistsAp(db.Model): # MedicalAssistant < assistsAp > Appointment
    __tablename__ = 'assistsAp'

    idAp: int
    ciPa: int
    ciMa: int
    time: datetime

    idAp = db.Column(db.Integer, db.ForeignKey(Appointment.id, ondelete='CASCADE'), primary_key=True)
    ciPa = db.Column(db.Integer, db.ForeignKey(Patient.ci, ondelete='CASCADE'), primary_key=True)
    ciMa = db.Column(db.Integer, db.ForeignKey(MedicalAssitant.ci, ondelete='CASCADE'), primary_key=True)
    time = db.Column(db.Time, primary_key=True)

@dataclass
class AttendsTo(db.Model): # Patient < attendsTo > [ Doctor < assignedTo > Appointment]
    __tablename__ = 'attendsTo'

    idAp: int
    ciPa: int
    motive: str
    number: int
    time: time

    idAp = db.Column(db.Integer, db.ForeignKey(Appointment.id, ondelete='CASCADE'), primary_key=True)
    ciPa = db.Column(db.Integer, db.ForeignKey(Patient.ci, ondelete='CASCADE'), primary_key=True)
    motive = db.Column(db.VARCHAR(256))
    number = db.Column(db.Integer) # an appointment could either be managed with numbers, or time-based turns, or both. 
    time = db.Column(db.Time)

@dataclass
class apRefPrevAp(db.Model): # auto-relationship, used to make reference to a previous appointment
    __tablename__ = 'apRefPrevAp'

    idCurrAp: int
    idPrevAp: int
    ciPaCurrAp: int
    ciPaPrevAp: int

    idCurrAp = db.Column(db.Integer, db.ForeignKey(Appointment.id, ondelete='CASCADE'), primary_key=True)
    idPrevAp = db.Column(db.Integer, db.ForeignKey(Appointment.id, ondelete='CASCADE'), primary_key=True)
    ciPaCurrAp = db.Column(db.Integer, db.ForeignKey(Patient.ci, ondelete='CASCADE'), primary_key=True)
    ciPaPrevAp = db.Column(db.Integer, db.ForeignKey(Patient.ci, ondelete='CASCADE'), primary_key=True)