from dataclasses import dataclass
from . import db
from .User import User
from datetime import datetime

@dataclass
class Vaccine(db.Model):
    ID: int
    name: str
    validity: int # in days

    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), unique=True, nullable=False) 
    validity = db.Column(db.Integer)

@dataclass
class UTakesVaccine(db.Model): # user < uTakesVaccine > Vaccine
    __tablename__ = 'uTakesVaccine'

    IDVaccine: int
    CIUser: int
    date: datetime

    IDVaccine = db.Column(db.Integer, db.ForeignKey(Vaccine.ID, ondelete='CASCADE'), primary_key=True)
    CIUser = db.Column(db.Integer, db.ForeignKey(User.CI, ondelete='CASCADE'), primary_key=True)
    date = db.Column(db.DateTime, primary_key=True, nullable=False)
