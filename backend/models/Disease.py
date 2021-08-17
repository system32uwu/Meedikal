from dataclasses import dataclass
from . import db

@dataclass
class Disease(db.Model):
    ID: int
    name: str
    description: str

    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), unique=True, nullable=False) 
    description = db.Column(db.VARCHAR(512)) 

@dataclass
class Category(db.Model):
    ID: int
    name: str

    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), unique=True, nullable=False) 

@dataclass
class DiseaseCat(db.Model): # Disease <diseaseCat> Category
    __tablename__ = 'diseaseCat'

    IDDisease: int
    IDCat: int

    IDDisease = db.Column(db.Integer, db.ForeignKey(Disease.ID, ondelete='CASCADE'), primary_key=True)
    IDCat = db.Column(db.Integer, db.ForeignKey(Category.ID, ondelete='CASCADE'), primary_key=True) 
