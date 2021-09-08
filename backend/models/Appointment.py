from dataclasses import dataclass
from datetime import datetime, date, time
from typing import Optional

appointmentStates = ('OK','CANCELLED', 'RESCHEDULING')

@dataclass
class Appointment:
    __tablename__ = 'appointment'

    id: int
    name: str
    state: str
    date: date

    timeBegins: Optional[time] = None
    timeEnds: Optional[time] = None
    etpp: Optional[int] = None # estimated time per patient, in seconds
    maxTurns: Optional[int] = None # max patients to be attended

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

    motive: Optional[str] = None
    number: Optional[int] = None
    time: Optional[time] = None