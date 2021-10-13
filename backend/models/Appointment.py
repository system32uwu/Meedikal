from ._base import BaseModel, TableWithId
from dataclasses import dataclass
from datetime import datetime, date as d
from typing import Optional

appointmentStates = ('OK','CANCELLED', 'RESCHEDULING')

@dataclass
class Appointment(BaseModel, TableWithId):
    __tablename__ = 'appointment'

    id:int
    name:str
    state:str
    date:d

    startsAt:Optional[datetime] = None
    endsAt:Optional[datetime] = None
    etpp:Optional[int] = None # estimated time per patient, in seconds
    maxTurns:Optional[int] = None # max patients to be attended

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

    def __init__(self,idAp:int,ciMa:int,time:str):
        self.idAp = idAp
        self.ciMa = ciMa
        self.time = datetime.fromisoformat(time)

@dataclass
class AttendsTo(BaseModel): # Patient < attendsTo > [ Doctor < assignedTo > Appointment]
    __tablename__ = 'attendsTo'

    idAp: int
    ciPa: int

    motive: Optional[str] = None
    time: Optional[datetime] = None
    number: Optional[int] = None

    def __init__(self,idAp:int,ciPa:int,motive:str=None,time:str=None, number:int=None):
        self.idAp = idAp
        self.ciPa = ciPa
        self.motive = motive
        try:
            self.time = datetime.fromisoformat(time)
        except:
            self.time = None
            
        self.number = number 