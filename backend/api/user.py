from werkzeug.security import generate_password_hash
from util.crud import crudReturn
from dataclasses import asdict

from flask import Blueprint, json, request, Request

from models.Specialty import *
from models.User import *
from util.returnMessages import *
from util.createDb import getDb
router = Blueprint('user', __name__, url_prefix='/user')

def getTypes(ci):
    types = [User.__tablename__]

    if Administrative.getByCi(ci) is not None:
        types.append(Administrative.__tablename__)
    
    if Patient.getByCi(ci) is not None:
        types.append(Patient.__tablename__)
    
    if MedicalPersonnel.getByCi(ci) is not None:
        types.append(MedicalPersonnel.__tablename__)
    
        if Doctor.getByCi(ci) is not None:
            types.append(Doctor.__tablename__)
        
        elif MedicalAssitant.getByCi(ci) is not None:
            types.append(MedicalAssitant.__tablename__)
    
    return types

def filterByType(userType=None, request:Request=None) -> list[User]:
    if request is not None:
        try:
            userType = request.get_json()['user'].get('userType', None)
        except:
            userType = None
    if userType == None:
        return User.query()
    else:
        return User.filter({'user.ci': f'{userType}.ci'})

def userToReturn(user: User, userType=None):
    if user is None:
        return None

    obj = {'user': asdict(user), 
           'types': getTypes(user.ci),
           'phoneNumbers': [asdict(p) for p in UserPhone.getByCi(user.ci)]}

    if userType == 'medicalPersonnel' or userType == 'doctor' or userType == 'medicalAssitant':
        hasSpec = MpHasSpec.query({'ciMp': user.ci})
        obj['specialties'] = [asdict(Specialty.filter({'id': id})) for id in 
                             [sp for sp in hasSpec]]

    obj['user'].pop('password', None)

    return obj

@router.errorhandler(Exception) 
def handle_exception(e:Exception):
    _e = repr(e)
    print(_e)
    getDb().rollback()
    if "object is not subscriptable" in _e:
        return provideData()
    elif "object has no attribute" in _e:
        return recordDoesntExist()
    elif "UNIQUE" in _e:
        return recordAlreadyExists()
    else:
        return {"error": repr(_e)}, 400


@router.get('/all') # GET /api/user/all
def allUsers():
    users = filterByType(request=request)
    return crudReturn([userToReturn(u) for u in users])

@router.post('') # POST /api/user
def createUser():
    data = json.loads(request.data)
    
    if data.get('password', None) is not None: # encrypt the password
        data['password'] = generate_password_hash(data['password'])

    result = User(**data).save()
    return crudReturn(userToReturn(result))

@router.get('') # GET /api/user
def getUserByCi():
    u = User.getByCi(request.get_json()['ci'])
    return crudReturn(userToReturn(u))

@router.delete('') # DELETE /api/user
def deleteUserByCi():
    result = User.delete(request.get_json()['ci'])
    return crudReturn(User, result, request=request)

@router.route('', methods=['PUT', 'PATCH']) # PUT | PATCH /api/user
def update():
    data = json.loads(request.data)
    
    if data.get('password', None) is not None: # encrypt the password
        if data['password'].get('value', None) is not None:
            data['password']['value'] = generate_password_hash(data['password']['value'])
        if data['password'].get('newValue', None) is not None:
            data['password']['newValue'] = generate_password_hash(data['password']['newValue'])

    result = User.update(data)
    return crudReturn([userToReturn(u) for u in result])

# @router.get('/surname1') # GET /api/user/surname1
# def userBySurname1():
#     data = json.loads(request.data)['user']
#     users = filterByType(request=request).filter(User.surname1 == data['surname1']).all()
#     return crudv2(User, preparedResult=[userToReturn(u) for u in users], jsonReturn=True)

# @router.get('/name1surname1') # GET /api/user/name1surname1
# def userByName1nSurname1():
#     data = json.loads(request.data)['user']
#     users = filterByType(request=request).filter(and_(
#                                             User.surname1 == data['surname1'],
#                                             User.name1 == data['name1'])).all()

#     return crudv2(User, preparedResult=[userToReturn(u) for u in users], jsonReturn=True)

# @router.route('', methods=['POST', 'PUT', 'PATCH']) # POST | PUT | PATCH /api/user
# def create_or_update():
#     return crudv2(User, request)

# @router.route('/patient', methods=['POST', 'DELETE']) # create or delete patient table
# def patient():
#     return crudv2(Patient, request)

# @router.route('/medicalPersonnel', methods=['POST', 'DELETE']) # create or delete medicalPersonnel | doctor | medicalassistant user
# def medicalPersonnel():
#     return crudv2(MedicalPersonnel,request)

# @router.route('/doctor', methods=['POST', 'DELETE']) # create or delete medicalPersonnel | doctor | medicalassistant user
# def doctor():
#     return crudv2(Doctor,request)

# @router.route('/medicalAssistant', methods=['POST', 'DELETE']) # create or delete medicalPersonnel | doctor | medicalassistant user
# def medicalAssistant():
#     return crudv2(MedicalAssitant,request)

# @router.route('/phoneNumbers', methods=['POST', 'DELETE', 'GET'])
# def phoneNumbers():
#     return crudv2(UserPhone,request)

# @router.route('/medicalPersonnel/mpHasSpec', methods=['POST','GET', 'DELETE'])
# def specialties(): #1 create / get specialties first, then add to MpHasSpec
#     if request.method == 'POST':
#         data = json.loads(request.data)
#         mpHasSpec = data['mpHasSpec']

#         _specialties = [getOrCreate(Specialty, Specialty(title=sp['title']),
#                         f"title = '{sp['title']}'") for sp in mpHasSpec]

#         for sp in _specialties:
#                 for _mpSpec in mpHasSpec:
#                     if _mpSpec['title'] == sp[0][0].title:
#                         _mpSpec['idSpec'] = sp[0][0].id
#                     _mpSpec.pop('title', None)

#         request.data = json.dumps({MpHasSpec.__tablename__: mpHasSpec})
    
#     return crudv2(MpHasSpec,request)

# @router.get('/medicalPersonnel/specialties') # get specialties of mp user
# def getSpecialtiesOfMp():
#     _specialties = MpHasSpec.query.filter(MpHasSpec.ciMp == json.loads(request.data)['user']['ci']).all()

#     __specialties = [asdict(Specialty.query.filter(Specialty.id == sp.idSpec).first())
#                     for sp in _specialties]

#     return crudv2(request=request,preparedResult=__specialties)

# @router.get('/medicalPersonnel/specialty') # GET /api/user/medicalPersonnel/specialty get medicalpersonnel users by specialty
# def getMedicalPersonnelBySpecialty():
#     data = json.loads(request.data)

#     specialty = Specialty.query.filter(Specialty.title == data['specialty']).one_or_none()

#     if specialty is None:
#         return recordDoesntExist(Specialty.__tablename__)
#     else:
#         specialtyId = specialty.id

#     users = filterByType(data['user']['userType']).filter(and_(
#                                             MpHasSpec.idSpec == specialtyId,
#                                             MpHasSpec.ciMp == User.ci 
#                                             )).all()

#     return crudv2(request=request, preparedResult=[userToReturn(u, userType=data['user']['userType']) for u in users])