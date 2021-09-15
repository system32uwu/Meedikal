from models.db import BaseModel, TableWithId
from dataclasses import dataclass
from datetime import datetime, date as d
from typing import Optional

appointmentStates = ('OK','CANCELLED', 'RESCHEDULING')

@dataclass
class Appointment(BaseModel, TableWithId):
    __tablename__ = 'appointment'

    id: int
    name: str
    state: str
    date: d

    startsAt: Optional[datetime] = None
    endsAt: Optional[datetime] = None
    etpp: Optional[int] = None # estimated time per patient, in seconds
    maxTurns: Optional[int] = None # max patients to be attended

    def __init__(self, id:int=None, name:str=None,state:str=None,date:str=None,
                startsAt:str=None, endsAt:str=None, etpp:int=None, maxTurns:int=None):
        self.id = id
        self.name = name
        self.state = state
        self.date = d.fromisoformat(date) if date is not None else None
        self.startsAt = datetime.fromisoformat(startsAt) if startsAt is not None else None
        self.endsAt = datetime.fromisoformat(endsAt) if endsAt is not None else None
        self.etpp = etpp
        self.maxTurns = maxTurns

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
    time: Optional[datetime] = None

    def __init__(self,idAp:int,ciPa:int,motive:str=None,number:int=None,time:str=None):
        self.idAp = idAp
        self.ciPa = ciPa
        self.motive = motive
        self.number = number
        self.time = datetime.fromisoformat(time) if time is not None else None