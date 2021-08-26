from dataclasses import asdict
from models.Specialty import MpHasSpec, Specialty
from models.User import User, Patient, MedicalPersonnel, Doctor, MedicalAssitant, Administrative, UserPhone, UIsRelatedTo
from flask import json, jsonify, Blueprint, request
from sqlalchemy.orm.query import Query

from werkzeug.security import generate_password_hash

from sqlalchemy import and_, or_

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

def removePassword(user): # remove the password before returning the object
    user.pop('password', None)

def userToReturn(user: User, userType=None):

    obj = {"user": asdict(user), 
           "phoneNumbers": [asdict(p) for p in UserPhone.query.filter(
                                    UserPhone.ci == user.ci).all()],
           "relatives": [asdict(r) for r in UIsRelatedTo.query.filter(or_(
                                    UIsRelatedTo.user1==user.ci,
                                    UIsRelatedTo.user2==user.ci)).all()]}

    if userType == 'medicalPersonnel':
        obj['specialties'] = [asdict(sp) for sp in Specialty.query.filter(and_(
                                        MpHasSpec.ciMp == user.ci,
                                        MpHasSpec.idSpec == Specialty.id)).all()]
    removePassword(obj['user'])

    return obj

@router.route('/all') # GET /api/user/all/{userType}
@router.route('/all/<userType>')
def allUsers(userType=None):
    users = filterByType(userType).all()
    usersToReturn = []
    
    for user in users:
        usersToReturn.append(userToReturn(user, userType))

    return jsonify(usersToReturn), 200

@router.route('/<int:ci>', methods=['GET','DELETE']) # GET | DELETE /api/user/{ci}
def userByCi(ci):
    user = filterByType(None).filter(User.ci == ci).first()
    if user is None:
        return recordDoesntExists("user")
    else:
        if request.method == 'GET':
            return jsonify(userToReturn(user)), 200
        else:
            user.delete()
            return recordCUDSuccessfully(delete=True)

@router.route('/<surname1>/<userType>') # GET /api/user/{surname1}/{userType}
def userBySurname1(surname1, userType=None):
    users = filterByType(userType).filter(User.surname1 == surname1).all()
    usersToReturn = []

    for user in users:
        usersToReturn.append(userToReturn(user, userType))

    return jsonify(usersToReturn), 200

@router.route('/<name1>/<surname1>/<userType>') # GET /api/user/{name1}/{surname1}/{userType}
def userByName1nSurname1(name1,surname1, userType=None):
    users = filterByType(userType).filter(and_(
                                            User.surname1 == surname1,
                                            User.name1 == name1)).all()
    usersToReturn = []
    
    for user in users:
        usersToReturn.append(userToReturn(user, userType))

    return jsonify(usersToReturn), 200

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
            get_or_create(model=UserPhone, 
                          toInsert=UserPhone(ci=user.ci,phone=phone),
                          ci=user.ci, phone=phone)

        relatives = userData['relatedTo']
        
        if request.method == 'PUT': # since put replaces, delete everything and then add whatever was sent
            delete(UIsRelatedTo,user1=user.ci)
            delete(UIsRelatedTo,user2=user.ci)
        
        for relative in relatives:
            get_or_create(model=UIsRelatedTo, 
                          toInsert=UIsRelatedTo(user1=user.ci,
                                                user2=relative.ci,
                                                typeUser1=relative.typeUser1,
                                                typeUser2=relative.typeUser2),
                          user1=user.ci, user2=relative.ci)

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

# -- MEDICAL PERSONNEL USERS

@router.route('/mp/<int:specialtyId>') # GET /api/user/mp/{specialtyId}
def medicalPersonnelBySpecialty(specialtyId:int):
    userType = 'medicalPersonnel'
    users = filterByType(userType).filter(and_(
                                            MpHasSpec.idSpec == specialtyId,
                                            MpHasSpec.ciMp == User.ci 
                                            )).all()
    usersToReturn = []
    
    for user in users:
        usersToReturn.append(userToReturn(user, userType))

    return jsonify(usersToReturn), 200