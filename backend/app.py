from dataclasses import dataclass

from flask import Flask, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from werkzeug.security import generate_password_hash, check_password_hash

from config import DevelopmentConfig

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)

migrate = Migrate(app,db)

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

    
@app.route("/")
def hello():
    
    u = User(
            CI=57681923, name1='carlos', name2='jose',
            surname1='gomez', surname2='gutierrez', sex='M',
            genre='male', password=generate_password_hash('testpwd')
            )

    db.session.add(u)
    db.session.commit()

    return jsonify(u)

if __name__ == '__main__':
    app.run()
