from dataclasses import dataclass
from datetime import datetime, date, time

appointmentStates = ('OK','CANCELLED', 'RESCHEDULING')

@dataclass
class Appointment:
    __tablename__ = 'appointment'

    id: int
    name: str
    date: date
    state: str
    timeBegins: time
    timeEnds: time
    etpp: int # estimated time per patient, in seconds
    maxTurns: int # max patients to be attended

@dataclass
class AssignedTo: # Doctor < assignedTo > Appointment
    __tablename__ = 'assignedTo'

    idAp: int
    ciDoc: int

@dataclass
class AssistsAp: # MedicalAssistant < assistsAp > [ Doctor < assignedTo > Appointment ]
    __tablename__ = 'assistsAp'

    idAp: int
    ciMa: int
    time: datetime

@dataclass
class AttendsTo: # Patient < attendsTo > [ Doctor < assignedTo > Appointment]
    __tablename__ = 'attendsTo'

    idAp: int
    ciPa: int
    motive: str
    number: int
    time: time