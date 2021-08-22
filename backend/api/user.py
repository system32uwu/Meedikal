from flask import json, jsonify, Blueprint, request
from sqlalchemy.orm.query import Query
from models.User import User, Patient, Administrative, Doctor, MedicalAssitant, MedicalPersonnel
from sqlalchemy import and_

router = Blueprint('user', __name__, url_prefix='/user')

# -- Base User entities

def filterByType(userType=None) -> Query:
    
    if userType == None:
        return User.query
    elif userType == 'patient':
        return User.query.filter(User.ci == Patient.ci)
    elif userType == 'medicalPersonnel':
        return User.query.filter(User.ci == MedicalPersonnel.ci)
    elif userType == 'doctor':
        return User.query.filter(User.ci == Doctor.ci)
    elif userType == 'medicalAssistant':
        return User.query.filter(User.ci == MedicalAssitant.ci)
    elif userType == 'administrative':
        return User.query.filter(User.ci == Administrative.ci)

@router.route('/all') # GET /api/user/all/{userType}
@router.route('/all/<userType>')
def allUsers(userType=None):
    return jsonify(filterByType(userType).all())

@router.route('/<int:ci>') # GET /api/user/{ci}
def userByCi(ci):
    return jsonify(filterByType(None).filter(User.ci == ci).first())

@router.route('/<surname1>/<userType>') # GET /api/user/{surname1}/{userType}
def userBySurname1(surname1, userType=None):
    return jsonify(filterByType(userType).filter(
                                                User.surname1 == surname1)
                                                .all())

@router.route('/<name1>/<surname1>/<userType>') # GET /api/user/{name1}/{surname1}/{userType}
def userByName1nSurname1(name1,surname1, userType=None):
    return jsonify(filterByType(userType)
                                        .filter(and_(
                                            User.surname1 == surname1,
                                            User.name1 == name1)).all())


# -- Patient entities 