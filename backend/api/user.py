from dataclasses import asdict

from models.Specialty import *
from models.User import *

from flask import json, jsonify, Blueprint, request
from sqlalchemy.orm.query import Query

from werkzeug.security import generate_password_hash

from sqlalchemy import and_, or_

from util.crud import *
from util.returnMessages import *

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

def userToReturn(user: User, userType=None, relationType=None):

    if user is None:
        return None

    obj = {'user': asdict(user), 
           'phoneNumbers': [asdict(p) for p in UserPhone.query.filter(
                                    UserPhone.ci == user.ci).all()],
           'relatives': [asdict(r) for r in UIsRelatedTo.query.filter(
                                    UIsRelatedTo.user1==user.ci).all()]}

    if userType == 'medicalPersonnel':
        obj['specialties'] = [asdict(sp) for sp in Specialty.query.filter(and_(
                                        MpHasSpec.ciMp == user.ci,
                                        MpHasSpec.idSpec == Specialty.id)).all()]

    if relationType is not None:
        obj['relationType'] = relationType

    removePassword(obj['user'])

    return obj

@router.get('/all') # GET /api/user/all/{userType}
@router.get('/all/<userType>')
def allUsers(userType=None):
    users = filterByType(userType).all()
    return crud(operation=request.method, model=User, 
                obj=[userToReturn(u) for u in users], jsonReturn=True)

@router.route('/<int:ci>/<userType>', methods=['GET','DELETE']) # GET | DELETE /api/user/{ci}
def userByCi(ci:int, userType:str):
    user = userToReturn(filterByType(None).filter(User.ci == ci).first(), userType=userType)
    return crud(operation=request.method,model=User,obj=user,
                jsonReturn=True, ci=user.ci)

@router.get('/<surname1>/<userType>') # GET /api/user/{surname1}/{userType}
def userBySurname1(surname1, userType=None):
    users = filterByType(userType).filter(User.surname1 == surname1).all()
    return crud(operation=request.method, model=User, 
                obj=[userToReturn(u) for u in users], jsonReturn=True)

@router.get('/<name1>/<surname1>/<userType>') # GET /api/user/{name1}/{surname1}/{userType}
def userByName1nSurname1(name1,surname1, userType=None):
    users = filterByType(userType).filter(and_(
                                            User.surname1 == surname1,
                                            User.name1 == name1)).all()

    return crud(operation=request.method, model=User, 
                obj=[userToReturn(u) for u in users], jsonReturn=True)

@router.route('', methods=['POST', 'PUT', 'PATCH']) # POST | PUT | PATCH /api/user
def create_or_update():

    try:
        userData = json.loads(request.data)

        u = User(ci=userData['ci'], name1=userData['name1'], name2=userData.get('name2', None),
                    surname1=userData['surname1'], surname2=userData.get('surname2', None), 
                    sex=userData['sex'], genre=userData.get('genre', None), 
                    birthdate=userData['birthdate'], location=userData['location'],
                    email=userData['email'], active=userData['active'],
                    password=generate_password_hash(userData['password']))

        return crud(operation=request.method, model=User, obj=u, ci=userData['ci'])

        relatives = userData['relatedTo']
        
        if request.method == 'PUT': # since put replaces, delete everything and then add whatever was sent
            delete(UIsRelatedTo,user1=user.ci)
            delete(UIsRelatedTo,user2=user.ci)
        
        for relative in relatives:
            getOrCreate(model=UIsRelatedTo, 
                          toInsert=UIsRelatedTo(user1=user.ci,
                                                user2=relative.ci,
                                                typeUser1=relative.typeUser1,
                                                typeUser2=relative.typeUser2),
                          user1=user.ci, user2=relative.ci)

        if userData['userType'] == 'patient':
            getOrCreate(model=Patient, toInsert=Patient(ci=user.ci), ci=user.ci)
        elif userData['userType'] == 'medicalPersonnel':
            mp, _created = (getOrCreate(model=MedicalPersonnel, toInsert=MedicalPersonnel(ci=user.ci), ci=user.ci))
            
            if request.method == 'PUT': # since put replaces, delete everything and then add whatever was sent
                delete(MpHasSpec,ciMp=mp.ci)

            for specialty in userData['specialties']:
                spec, __created = (getOrCreate(model=Specialty, toInsert=Specialty(title=specialty['title']), title=specialty['title']))
                getOrCreate(model=MpHasSpec, toInsert=MpHasSpec(idSpec=spec.id, ciMp=mp.ci, detail=specialty['detail']), idSpec=spec.id, ciMp=mp.ci)
            
            if userData['subType'] == 'doctor':
                getOrCreate(model=Doctor, toInsert=Doctor(ci=mp.ci), ci=mp.ci)
            elif userData['subType'] == 'medicalAssistant':
                getOrCreate(model=MedicalAssitant, toInsert=MedicalAssitant(ci=mp.ci), ci=mp.ci)

            if request.method == 'POST':
                return recordCUDSuccessfully('user',create=True)
            else:
                return recordCUDSuccessfully('user',update=True)
    except:
        return provideData()

@router.route('/phoneNumbers', methods=['POST','PUT','PATCH'])
def phoneNumbers():
    try:
        data = json.loads(request.data)
        phones = [UserPhone(ci=p.ci,phone=p.phone) for p in data]
        return crud(operation=request.method,model=UserPhone,obj=phones,deleteBeforeUpdate=True)
    except:
        return provideData()

@router.get('/phoneNumbers/<int:ci>')
def getPhoneNumbers(ci:int):
    phones = UserPhone.query.filter(UserPhone.ci == ci).all()
    return crud(operation=request.method,model=UserPhone,obj=phones,
                jsonReturn=True,ci=ci)

@router.route('/relatives', methods=['POST','PUT','PATCH'])
def relatives():
    try:
        data = json.loads(request.data)
        _relatives = [UIsRelatedTo(user1=relative.user1, user2=relative.user2,
                               typeUser1=relative.typeUser1,
                               typeUser2=relative.typeUser2,)
                               for relative in data]

        return crud(operation=request.method,model=UserPhone,obj=_relatives,deleteBeforeUpdate=True, user1=_relatives[0].user1)
    except:
        return provideData()

@router.get('/relatives/<int:ci>')
def getRelatives(ci:int):
    _relatives = UIsRelatedTo.query.filter(UIsRelatedTo.user1 == ci).all()
    #               user1 is <son> of user2
    __relatives = [userToReturn(user, 
                    relationType = next(r.relationType for r in _relatives
                                        if r.user2 == user.ci))
                    for user in 
                    [User.query.filter(User.ci==r.user2).first()
                     for r in _relatives]]

    return crud(operation=request.method,model=UIsRelatedTo,obj=__relatives,
                jsonReturn=True,ci=ci)

# -- MEDICAL PERSONNEL USERS
@router.get('/mp/<subType>/<specialty>') # GET /api/user/mp/{subType}/{specialtyId}
def medicalPersonnelBySpecialty(subType:str,specialty:str):
    specialty = Specialty.query.filter(Specialty.title == specialty).first()

    if specialty is None:
        return recordDoesntExist(Specialty.__tablename__)
    else:
        specialtyId = specialty.id

    users = filterByType(subType).filter(and_(
                                            MpHasSpec.idSpec == specialtyId,
                                            MpHasSpec.ciMp == User.ci 
                                            )).all()

    return crud(operation=request.method, model=User, 
                obj=[userToReturn(u) for u in users], jsonReturn=True)