from werkzeug.security import generate_password_hash
from util.crud import crudReturn
from dataclasses import asdict

from flask import Blueprint, json, request, Request

from models.Specialty import *
from models.User import *

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

def filterByType(userType=None, request:Request=None, dictReturn=False):
    try:
        data = json.loads(request.data)
    except:
        data = {}

    userType = data.get('userType', None)

    if userType == None and not dictReturn:
        return User.query()
    elif userType == None and dictReturn:
        return data
    else:
        userTypeFilter = {'user.ci': f'{userType}.ci'}
        if dictReturn:
            if data is not None:
                data.pop('userType')
                conditionList = dict(list(data.items()) + list(userTypeFilter.items()))
                return conditionList
            else:
                return userTypeFilter
        else:
            return User.filter(userTypeFilter)

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

@router.route('/all', methods=['GET', 'POST']) # GET | POST /api/user/all
def allUsers():
    users = filterByType(request=request)
    return crudReturn([userToReturn(u) for u in users])

@router.post('') # POST /api/user
@router.get('/<int:ci>') # GET /api/user/<ci>
def getUserByCi(ci:int=None):
    if ci is None: # if ci is None the method used was POST.
        ci = request.get_json()['ci']

    u = User.getByCi(ci)
    return crudReturn(userToReturn(u))

@router.post('') # POST /api/user
def createUser():
    data = json.loads(request.data)
    
    if data.get('password', None) is not None: # encrypt the password
        data['password'] = generate_password_hash(data['password'])

    result = User(**data).save()
    return crudReturn(userToReturn(result))

@router.delete('') # DELETE /api/user
def deleteUserByCi():
    result = User.delete(request.get_json()['ci'])
    return crudReturn(result)

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

@router.post('/surname1') # POST /api/user/surname1 filter by surname1 and userType
@router.get('/<surname1>') # GET /api/user/<surname1> filter only by surname1
def userBySurname1(surname1:str=None):
    if surname1 is None:
        conditionList = filterByType(request=request,dictReturn=True)
    else:
        conditionList = {'surname1' : surname1}

    return crudReturn([userToReturn(u) for u in User.filter(conditionList)])

@router.post('/name1surname1') # GET /api/user/name1surname1
@router.get('/<name1>/<surname1>') # GET /api/user/<name1>/<surname1>
def userByName1nSurname1(name1:str=None,surname1:str=None):
    if name1 is None and surname1 is None:
        conditionList = filterByType(request=request,dictReturn=True)
    else:
        conditionList = {'name1': name1, 'surname1' : surname1}

    return crudReturn([userToReturn(u) for u in User.filter(conditionList)])

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