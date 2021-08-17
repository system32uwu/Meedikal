from .User import MedicalPersonnel
from dataclasses import dataclass
from . import db
from datetime import datetime

@dataclass
class Form(db.Model):

    ID: int
    title: str
    preview: str # path of a screenshot of the form
    content: object # serialized components (labels, input fields, checkboxes...)

    ID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(64)) 
    preview = db.Column(db.String())
    content = db.Column(db.JSON)

@dataclass
class Question(db.Model):

    ID: int
    text: str

    ID = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.VARCHAR(64), nullable=False) 

@dataclass # question < from > form
class From(db.Model):

    IDQ: int # id of the question
    IDF: str # id of the form

    IDQ = db.Column(db.Integer, db.ForeignKey(Question.ID, ondelete='CASCADE'), primary_key=True)
    IDF = db.Column(db.Integer, db.ForeignKey(Form.ID, ondelete='CASCADE'), primary_key=True)

@dataclass # medicalPersonnel user < designed > form
class Designed(db.Model):

    CIMP: int # id of the user
    IDF: str # id of the form
    date: datetime # date and time the form is created / updated
    isMainAuthor: bool # if the user is the creator of the form
    changelog: str # log what was added or removed, like version control with git.

    CIMP = db.Column(db.Integer, db.ForeignKey(MedicalPersonnel.CI, ondelete='CASCADE'), primary_key=True)
    IDF = db.Column(db.Integer, db.ForeignKey(Form.ID, ondelete='CASCADE'), primary_key=True)
    date = db.Column(db.DateTime, primary_key=True, nullable=False)
    isMainAuthor = db.Column(db.BOOLEAN, default=True, nullable=False)
    changelog = db.Column(db.String())
