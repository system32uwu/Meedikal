from dataclasses import dataclass
from werkzeug.security import check_password_hash
from . import db

@dataclass
class User(db.Model):

    CI: int
    name1: str
    name2: str
    surname1: str
    surname2: str
    sex: str
    genre: str
    password: str

    CI = db.Column(db.Integer, primary_key=True)
    name1 = db.Column(db.String(32), nullable=False)
    name2 = db.Column(db.String(32))
    surname1 = db.Column(db.String(32), nullable=False)
    surname2 = db.Column(db.String(32))
    sex = db.Column(db.String(1), default='M', nullable=False)
    genre = db.Column(db.String(16), default='Male')
    password = db.Column(db.String(128), nullable=False)        

    def check_password(self, password) -> bool:
        return check_password_hash(self.password, password)