from models.Specialty import MpHasSpec, Specialty
from models.User import User, Patient, MedicalPersonnel, Doctor, MedicalAssitant, Administrative, UserPhone
from flask import json, jsonify, Blueprint, request
from sqlalchemy.orm.query import Query

from werkzeug.security import generate_password_hash

from sqlalchemy import and_

from .crud import get_or_create, put, patch, delete
from .returnMessages import provideData, recordAlreadyExists, recordCUDSuccessfully, recordDoesntExists, notFound

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

def userToReturn(user: User): # remove the password before returning the object
    delattr(user,'password')

@router.route('/all') # GET /api/user/all/{userType}
@router.route('/all/<userType>')
def allUsers(userType=None):
    users = filterByType(userType).all()
    [userToReturn(user) for user in users]   
    return jsonify(users), 200

@router.route('/<int:ci>', methods=['GET','DELETE']) # GET | DELETE /api/user/{ci}
def userByCi(ci):
    user = filterByType(None).filter(User.ci == ci).first()
    if user is None:
        return recordDoesntExists("user")
    else:
        if request.method == 'GET':
            userToReturn(user)
            return jsonify(user), 200
        else:
            user.delete()
            return recordCUDSuccessfully(delete=True)

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

@router.route('', methods=['POST', 'PUT', 'PATCH', 'DELETE']) # POST | PUT | PATCH /api/user
def create_or_update():

    try:
        userData = json.loads(request.data)

        u = User(ci=userData['ci'], name1=userData['name1'], name2=userData['name2'],
                    surname1=userData['surname1'], surname2=userData['surname2'], 
                    sex=userData['sex'], genre=userData['genre'], 
                    birthdate=userData['birthdate'], location=userData['location'],
                    email=userData['email'], active=userData['active'],
                    password=generate_password_hash(userData['password']))

        if request.method == 'POST':
            user, created = (get_or_create(model=User, toInsert=u, ci=userData['ci']))
            if not created:
                return recordAlreadyExists()
        elif request.method == 'PUT':
            user, putted = (put(model=User, toPut=u, ci=userData['ci']))
            if not putted:
                return recordDoesntExists()
        elif request.method == 'PATCH':
            user, patched = (patch(model=User, toPatch=u, ci=userData['ci']))
            if not patched:
                return recordDoesntExists()
        
        phones = userData['phoneNumbers']
        
        if request.method == 'PUT': # since put replaces, delete everything and then add whatever was sent
            delete(UserPhone,ci=user.ci)
        
        for phone in phones:
            get_or_create(model=UserPhone, toInsert=UserPhone(ci=user.ci,phone=phone), ci=user.ci, phone=phone)

        if userData['userType'] == 'patient':
            get_or_create(model=Patient, toInsert=Patient(ci=user.ci), ci=user.ci)
        elif userData['userType'] == 'medicalPersonnel':
            mp, _created = (get_or_create(model=MedicalPersonnel, toInsert=MedicalPersonnel(ci=user.ci), ci=user.ci))
            
            if request.method == 'PUT': # since put replaces, delete everything and then add whatever was sent
                delete(MpHasSpec,ciMp=mp.ci)

            for specialty in userData['specialties']:
                spec, __created = (get_or_create(model=Specialty, toInsert=Specialty(title=specialty['title']), title=specialty['title']))
                get_or_create(model=MpHasSpec, toInsert=MpHasSpec(idSpec=spec.id, ciMp=mp.ci, detail=specialty['detail']), idSpec=spec.id, ciMp=mp.ci)
            
            if userData['subType'] == 'doctor':
                get_or_create(model=Doctor, toInsert=Doctor(ci=mp.ci), ci=mp.ci)
            elif userData['subType'] == 'medicalAssistant':
                get_or_create(model=MedicalAssitant, toInsert=MedicalAssitant(ci=mp.ci), ci=mp.ci)

            if request.method == 'POST':
                return recordCUDSuccessfully("user",create=True)
            else:
                return recordCUDSuccessfully("user",update=True)
    except:
        return provideData()

@router.route("/<int:ci>/phoneNumbers")
def getUserPhoneNumbers(ci):
    return jsonify(UserPhone.query.filter(UserPhone.ci == ci).all()), 200

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