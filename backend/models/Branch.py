from .Appointment import Appointment
from dataclasses import dataclass
from . import db

@dataclass
class Branch(db.Model):

    id: int
    name: str
    phoneNumber: str
    location: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(64), unique=True, nullable=False) 
    phoneNumber = db.Column(db.VARCHAR(64), nullable=False) 
    location = db.Column(db.VARCHAR(64), nullable=False) 

@dataclass
class apTakesPlace(db.Model): # Appointment < apTakesPlace > Branch
    __tablename__ = 'apTakesPlace'

    idAp: int
    idBranch: int

    idAp = db.Column(db.Integer, db.ForeignKey(Appointment.id, ondelete='CASCADE'), primary_key=True)
    idBranch = db.Column(db.Integer, db.ForeignKey(Branch.id, ondelete='CASCADE'), primary_key=True)
