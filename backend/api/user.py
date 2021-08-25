# TODO (system32uwu): Ignore users' passwords on response
from models.Specialty import MpHasSpec, Specialty
from models.User import User, Patient, MedicalPersonnel, Doctor, MedicalAssitant, Administrative, UserPhone
from flask import json, jsonify, Blueprint, request
from sqlalchemy.orm.query import Query
from werkzeug.security import generate_password_hash
from sqlalchemy import and_
from models.db import get_or_create, put

router = Blueprint('user', __name__, url_prefix='/user')

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

def userToReturn(user):
    delattr(user,'password')

@router.route('/all') # GET /api/user/all/{userType}
@router.route('/all/<userType>')
def allUsers(userType=None):
    users = filterByType(userType).all()
    [userToReturn(user) for user in users]   
    return jsonify(users), 200

@router.route('/<int:ci>') # GET /api/user/{ci}
def userByCi(ci):
    user = filterByType(None).filter(User.ci == ci).first()
    userToReturn(user)
    return jsonify(user), 200

@router.route('/<surname1>/<userType>') # GET /api/user/{surname1}/{userType}
def userBySurname1(surname1, userType=None):
    users = filterByType(userType).filter(User.surname1 == surname1).all()
    [userToReturn(user) for user in users]  
    return jsonify(users), 200

@router.route('/<name1>/<surname1>/<userType>') # GET /api/user/{name1}/{surname1}/{userType}
def userByName1nSurname1(name1,surname1, userType=None):
    users = filterByType(userType).filter(and_(
                                            User.surname1 == surname1,
                                            User.name1 == name1)).all()
    [userToReturn(user) for user in users]
    return jsonify(users), 200

@router.route('', methods=['POST', 'PUT', 'PATCH']) # POST | PUT | PATCH /api/user
def new():

    if not request.data:
        return "provide user data", 400

    userData = json.loads(request.data)

    try:
        u = User(ci=userData['ci'], name1=userData['name1'], name2=userData['name2'],
                    surname1=userData['surname1'], surname2=userData['surname2'], 
                    sex=userData['sex'], genre=userData['genre'], 
                    birthdate=userData['birthdate'], location=userData['location'],
                    email=userData['email'], active=userData['active'],
                    password=generate_password_hash(userData['password']))

        created = False
        putted = False

        if request.method == 'POST':
            user, created = (get_or_create(model=User, toInsert=u, ci=userData['ci']))    
            if not created:
                return "user already exists", 400

        elif request.method == 'PUT':
            user, putted = (put(model=User, toPut=u, ci=userData['ci']))
            if not putted:
                return "user doesn't exist", 400
        # TODO: Add patch method in models.db
        # elif request.method == 'PATCH':
        #     user, patched = (patch(model=User, toPut=u, ci=userData['ci']))
        #     if not patched:
        #         return "user doesn't exist", 400
        
        phones = userData['phoneNumbers']

        for phone in phones:
            get_or_create(model=UserPhone, toInsert=UserPhone(ci=user.ci,phone=phone), ci=user.ci, phone=phone)

        if userData['userType'] == 'patient':
            get_or_create(model=Patient, toInsert=Patient(ci=user.ci), ci=user.ci)
        elif userData['userType'] == 'medicalPersonnel':
            mp, _created = (get_or_create(model=MedicalPersonnel, toInsert=MedicalPersonnel(ci=user.ci), ci=user.ci))
            
            for specialty in userData['specialties']:
                spec, __created = (get_or_create(model=Specialty, toInsert=Specialty(title=specialty['title']), title=specialty['title']))
                get_or_create(model=MpHasSpec, toInsert=MpHasSpec(idSpec=spec.id, ciMp=mp.ci, detail=specialty['detail']), idSpec=spec.id, ciMp=mp.ci)
            
            if userData['subType'] == 'doctor':
                get_or_create(model=Doctor, toInsert=Doctor(ci=mp.ci), ci=mp.ci)
            elif userData['subType'] == 'medicalAssistant':
                get_or_create(model=MedicalAssitant, toInsert=MedicalAssitant(ci=mp.ci), ci=mp.ci)

            if request.method == 'POST':
                return "user created successfully", 200
            else:
                return "user updated successfully", 200

    except Exception as exc:
        return {"error": exc.args}, 400

# -- MEDICAL PERSONNEL USERS

@router.route('/mp/<int:specialtyId>') # GET /api/user/mp/{specialtyId}
def medicalPersonnelBySpecialty(specialtyId:int):
    return jsonify(filterByType(userType='medicalPersonnel').filter(and_(
                                            MpHasSpec.idSpec == specialtyId,
                                            MpHasSpec.ciMp == User.ci 
                                            )).all()), 200

@router.route('/mp/<int:ci>/specialties') # GET /api/user/mp/{ci}/specialties
def medicalPersonnelSpecialties(ci:int):
    return jsonify(Specialty.query.filter(and_(
                                        MpHasSpec.ciMp == ci,
                                        MpHasSpec.idSpec == Specialty.id)).all()), 200