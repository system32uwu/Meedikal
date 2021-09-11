from models.db import BaseModel, TableWithId
from dataclasses import dataclass
from datetime import datetime, date, time
from typing import Optional

appointmentStates = ('OK','CANCELLED', 'RESCHEDULING')

@dataclass
class Appointment(BaseModel, TableWithId):
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
class AssignedTo(BaseModel): # Doctor < assignedTo > Appointment
    __tablename__ = 'assignedTo'

    idAp: int
    ciDoc: int

@dataclass
class AssistsAp(BaseModel): # MedicalAssistant < assistsAp > [ Doctor < assignedTo > Appointment ]
    __tablename__ = 'assistsAp'

    idAp: int
    ciMa: int
    time: datetime

@dataclass
class AttendsTo(BaseModel): # Patient < attendsTo > [ Doctor < assignedTo > Appointment]
    __tablename__ = 'attendsTo'

    idAp: int
    ciPa: int

    motive: Optional[str] = None
    number: Optional[int] = None
    time: Optional[time] = None