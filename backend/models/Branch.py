from .Treatment import TakesCare
from .Appointment import Appointment
from dataclasses import dataclass
from .db import db, BaseModel

@dataclass
class Branch(BaseModel):

    id: int
    name: str
    phoneNumber: str
    location: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(64), unique=True, nullable=False) 
    phoneNumber = db.Column(db.VARCHAR(64), nullable=False) 
    location = db.Column(db.VARCHAR(64), nullable=False) 

@dataclass
class ApTakesPlace(BaseModel): # Appointment < apTakesPlace > Branch
    __tablename__ = 'apTakesPlace'

    idAp: int
    idBranch: int

    idAp = db.Column(db.Integer, db.ForeignKey(Appointment.id, ondelete='CASCADE'), primary_key=True)
    idBranch = db.Column(db.Integer, db.ForeignKey(Branch.id, ondelete='CASCADE'))

@dataclass
class TrTakesPlace(BaseModel): # takesCare < trTakesPlace > Branch
    __tablename__ = 'trTakesPlace'

    idFollows: int
    idTreatment: int
    ciPa: int
    ciMp: int
    date: int
    idBranch: int

    idFollows = db.Column(db.Integer, primary_key=True)
    idTreatment = db.Column(db.Integer, primary_key=True)
    ciPa = db.Column(db.Integer, primary_key=True)
    ciMp = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, primary_key=True)
    idBranch = db.Column(db.Integer, db.ForeignKey(Branch.id, ondelete='CASCADE'))

    __table_args__ = (db.ForeignKeyConstraint([idFollows,idTreatment,ciPa,ciMp,date],[TakesCare.idFollows,TakesCare.idTreatment,TakesCare.ciPa,TakesCare.ciMp,TakesCare.date]),)
