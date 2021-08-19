from dataclasses import dataclass
from . import db
from .User import User
from datetime import datetime

@dataclass
class Vaccine(db.Model):
    id: int
    name: str
    validity: int # in days

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), unique=True, nullable=False) 
    validity = db.Column(db.Integer)

@dataclass
class UTakesVaccine(db.Model): # user < uTakesVaccine > Vaccine
    __tablename__ = 'uTakesVaccine'

    idVaccine: int
    ciUser: int
    date: datetime

    idVaccine = db.Column(db.Integer, db.ForeignKey(Vaccine.id, ondelete='CASCADE'), primary_key=True)
    ciUser = db.Column(db.Integer, db.ForeignKey(User.ci, ondelete='CASCADE'), primary_key=True)
    date = db.Column(db.DateTime, primary_key=True, nullable=False)
