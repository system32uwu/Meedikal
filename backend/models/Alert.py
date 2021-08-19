from .User import User
from dataclasses import dataclass
from . import db

@dataclass
class Alert(db.Model): # allergies, behaviours, traumas...

    ID: int
    title: str

    ID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(64), nullable=False) 

@dataclass
class UHasAlert(db.Model): # user < UHasAlert > Alert

    __tablename__ = 'uHasAlert'

    IDAlert: int
    CIUser: int
    detail: str

    IDAlert = db.Column(db.Integer, db.ForeignKey(Alert.ID, ondelete='CASCADE'), primary_key=True)
    CIUser = db.Column(db.Integer, db.ForeignKey(User.CI, ondelete='CASCADE'))
    detail = db.Column(db.VARCHAR(256), nullable=False) 