from dataclasses import dataclass
from . import db

@dataclass
class Medicine(db.Model):
    ID: int
    name: str
    description: str
    notes: str

    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), unique=True, nullable=False) 
    description = db.Column(db.String())
    notes = db.Column(db.String())

@dataclass
class Manufacturer(db.Model):

    ID: int
    name: str
    location: str
    email: str
    phoneNumber: str
    logo: str

    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), unique=True, nullable=False)
    location = db.Column(db.VARCHAR(256))
    email = db.Column(db.VARCHAR(256))
    phoneNumber = db.Column(db.VARCHAR(32))
    logo = db.Column(db.String())

@dataclass 
class ManufacturedBy(db.Model):
    __tablename__ = 'manufacturedBy'

    IDMed: int
    IDManufacturer: int

    IDMed = db.Column(db.Integer, db.ForeignKey(Medicine.ID, ondelete='CASCADE'), primary_key=True)
    IDManufacturer = db.Column(db.Integer, db.ForeignKey(Manufacturer.ID, ondelete='CASCADE'), primary_key=True)
    