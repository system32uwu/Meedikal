from dataclasses import asdict

from flask import json, Blueprint, request
from sqlalchemy import and_
from sqlalchemy.orm.query import Query

from werkzeug.security import generate_password_hash

from models.Specialty import *
from models.User import *
from util.crud import *
from util.returnMessages import *

router = Blueprint('user', __name__, url_prefix='/user')

def getTypes(ci):
    types = [User.__tablename__]

    if Administrative.query.filter(Administrative.ci==ci).one_or_none() is not None:
        types.append(Administrative.__tablename__)
    
    if Patient.query.filter(Patient.ci==ci).one_or_none() is not None:
        types.append(Patient.__tablename__)
    
    if MedicalPersonnel.query.filter(MedicalPersonnel.ci==ci).one_or_none() is not None:
        types.append(MedicalPersonnel.__tablename__)
    
        if Doctor.query.filter(Doctor.ci==ci).one_or_none() is not None:
            types.append(Doctor.__tablename__)
        
        elif MedicalAssitant.query.filter(MedicalAssitant.ci==ci).one_or_none() is not None:
            types.append(MedicalAssitant.__tablename__)
    
    return types

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

def userToReturn(user: User, userType=None, relationType=None):
    if user is None:
        return None

    obj = {'user': asdict(user), 
           'phoneNumbers': [asdict(p) for p in UserPhone.query.filter(
                                    UserPhone.ci == user.ci).all()],
           'relatives': [asdict(r) for r in UIsRelatedTo.query.filter(
                                    UIsRelatedTo.user1==user.ci).all()],
            'types': getTypes(user.ci)}

    if userType == 'medicalPersonnel' or userType == 'doctor' or userType == 'medicalAssitant':
        obj['specialties'] = [asdict(sp) for sp in Specialty.query.filter(and_(
                                        MpHasSpec.ciMp == user.ci,
                                        MpHasSpec.idSpec == Specialty.id)).all()]

    if relationType is not None:
        obj['relationType'] = relationType

    obj['user'].pop('password', None)

    return obj

@router.get('/all') # GET /api/user/all/{userType}
@router.get('/all/<userType>')
def allUsers(userType=None):
    users = filterByType(userType).all()
    return crud(operation=request.method, model=User, 
                obj=[userToReturn(u) for u in users], jsonReturn=True)

@router.route('/<int:ci>', methods=['GET','DELETE']) # GET | DELETE /api/user/{ci}
@router.route('/<int:ci>/<userType>', methods=['GET','DELETE']) # GET | DELETE /api/user/{ci}/{userType}
@router.route('/<int:ci>/<int:logicalCD>', methods=['GET','DELETE']) # GET | DELETE /api/user/{ci}/{logicalCD}
@router.route('/<int:ci>/<userType>/<int:logicalCD>', methods=['GET','DELETE']) # GET | DELETE /api/user/{ci}/{userType}/{logicalCD}
def userByCi(ci:int, userType:str=None, logicalCD:int=None): # logicalCD (logical Create / Delete) = set active to False or True (0,1)
    user = filterByType(userType).filter(User.ci == ci).first()
    if logicalCD is not None:
        if user is not None:
            user.update(active=bool(logicalCD))
    else:
        if user is not None:
            print(request.method)
            return crud(operation=request.method,model=User,obj=userToReturn(user), ci=user.ci,
                        jsonReturn= True if request.method == 'GET' else False, 
                        messageReturn= True if request.method == 'DELETE' else False )
        else:
            return recordDoesntExist(User.__tablename__)

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
        userData = json.loads(request.data) # ci is a mandatory field

        u = User(ci=userData['ci'], name1=userData.get('name1', None), name2=userData.get('name2', None),
                 surname1=userData.get('surname1', None), surname2=userData.get('surname2', None), 
                 sex=userData.get('sex', None), genre=userData.get('genre', None), 
                 birthdate=userData.get('birthdate', None), location=userData.get('location', None),
                 email=userData.get('email', None), active=userData.get('active', True),)
        
        if userData.get('password', None) is not None:
            u.password=generate_password_hash(userData['password']) # if password is not provided it raises an exception

        return crud(operation=request.method, model=User, obj=u, messageReturn=True, ci=userData['ci'])
    except:
        return provideData()

@router.route('/patient/<int:ci>', methods=['POST', 'DELETE']) # create or delete patient table
def patient(ci:int):
    return crud(request.method, model=Patient, obj=Patient(ci=ci),
                messageReturn=True,ci=ci)

@router.route('/mp/<int:ci>', methods=['POST', 'DELETE']) # create or delete patient table
@router.route('/mp/<int:ci>/<subType>', methods=['POST', 'DELETE']) # create or delete patient table
def medicalPersonnel(ci:int, subType=None):
    if subType is None:
        return crud(request.method, model=MedicalPersonnel, 
                    obj=MedicalPersonnel(ci=ci), messageReturn=True, ci=ci)
    else:
        mp, created = (crud(request.method, model=MedicalPersonnel, 
                            obj=MedicalPersonnel(ci=ci), tupleReturn=True, ci=ci))
    
        if not created:
            return recordAlreadyExists(MedicalPersonnel.__tablename__)
        else:
            if subType == 'doctor':
                return crud(request.method, model=Doctor, 
                            obj=Doctor(ci=mp.ci), messageReturn=True, ci=mp.ci)
            elif subType == 'medicalAssistant':
                return crud(request.method, model=MedicalAssitant, 
                            obj=MedicalAssitant(ci=ci), messageReturn=True, ci=mp.ci)
            else:
                return provideData()

@router.route('/phoneNumbers', methods=['POST','PUT','PATCH'])
def phoneNumbers():
    try:
        data = json.loads(request.data)
        phones = [UserPhone(ci=p['ci'],phone=p['phone']) for p in data['phones']]
        
        if request.method == 'PUT' or request.method == 'PATCH':
            delete(UserPhone,ci=phones[0].ci)
        
        for phone in phones:
            result, opState = (crud(operation='POST',model=UserPhone,
                               obj=phone, tupleReturn=True, ci=phone.ci, phone=phone.phone))
            if not opState:
                if request.method == 'POST':
                    return recordAlreadyExists(UserPhone.__tablename__, asdict(phone))

        return recordCUDSuccessfully(UserPhone.__tablename__, request.method)

    except Exception as exc:
        print(f"exc: {exc}")
        return provideData()

@router.get('/phoneNumbers/<int:ci>')
def getPhoneNumbers(ci:int):
    phones = [asdict(p) for p in UserPhone.query.filter(UserPhone.ci == ci).all()]
    return crud(operation=request.method,model=UserPhone,obj=phones,
                jsonReturn=True,ci=ci)

@router.route('/relatives', methods=['POST','PUT','PATCH'])
def relatives():
    try:
        data = json.loads(request.data)
        _relatives = [UIsRelatedTo(user1=relative['user1'], user2=relative['user2'],
                               relationType=relative['relationType'])
                               for relative in data['relatives']]

        if request.method == 'PUT' or request.method == 'PATCH':
            delete(UIsRelatedTo,user1=_relatives[0].user1)
        
        for r in _relatives:
            result, opState = (crud(operation='POST',model=UIsRelatedTo,
                               obj=r, tupleReturn=True, user1=r.user1, user2=r.user2))
            if not opState:
                if request.method == 'POST':
                    return recordAlreadyExists(UIsRelatedTo.__tablename__, asdict(r))

        return recordCUDSuccessfully(UIsRelatedTo.__tablename__, request.method)
    except:
        return provideData()

@router.get('/relatives/<int:ci>')
def getRelatives(ci:int):
    _relatives = UIsRelatedTo.query.filter(UIsRelatedTo.user1 == ci).all()
    #               user1 is <relationType> of user2
    __relatives = [userToReturn(user, 
                    relationType = next(r.relationType for r in _relatives
                                        if r.user2 == user.ci))
                    for user in 
                    [User.query.filter(User.ci==r.user2).first()
                     for r in _relatives]]

    return crud(operation=request.method,model=UIsRelatedTo,obj=__relatives,
                jsonReturn=True,ci=ci)

@router.get('/mp/specialties/<int:ci>') # get specialties of mp user
def getSpecialties(ci:int):
    _specialties = MpHasSpec.query.filter(MpHasSpec.ciMp == ci).all()

    __specialties = [Specialty.query.filter(Specialty.id == sp.idSpec).first()
                    for sp in _specialties]

    return crud(operation=request.method,model=Specialty,obj=__specialties,
                jsonReturn=True,ci=ci)

# -- MEDICAL PERSONNEL USERS
@router.get('/mp/<specialty>/<type>') # GET /api/user/mp/{specialtyName}/{mpUserType}
def medicalPersonnelBySpecialty(specialty:str, type:str):
    specialty = Specialty.query.filter(Specialty.title == specialty).one_or_none()

    if specialty is None:
        return recordDoesntExist(Specialty.__tablename__)
    else:
        specialtyId = specialty.id

    users = filterByType(type).filter(and_(
                                            MpHasSpec.idSpec == specialtyId,
                                            MpHasSpec.ciMp == User.ci 
                                            )).all()

    return crud(operation=request.method, model=User, 
                obj=[userToReturn(u, userType=type) for u in users], jsonReturn=True)