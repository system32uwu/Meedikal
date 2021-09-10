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

@router.get('/<int:ci>') # GET /api/user/<ci>
def getUserByCi(ci:int=None):
    if ci is None: # if ci is None the method used was POST.
        ci = request.get_json()['ci']

    u = User.getByCi(ci)
    return crudReturn(userToReturn(u))

@router.post('') # POST /api/user
def createUser():
    data = json.loads(request.data)
    
    data['password'] = generate_password_hash(data['password'])

    result = User(**data).save()

    return crudReturn(userToReturn(result))

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

@router.delete('') # DELETE /api/user
def deleteUserByCi():
    result = User.delete(request.get_json()['ci'])
    return crudReturn(result)

@router.route('/patient') # POST | DELETE /api/patient
def patient():
    p = Patient(request.get_json()['ci'])
    if request.method == 'POST':
        result = userToReturn(p.save())
    else:
        result = Patient.delete({'ci': p.ci})

    return crudReturn(result)

@router.route('/medicalPersonnel') # POST | DELETE /api/medicalPersonnel
def medicalPersonnel():
    mp = MedicalPersonnel(request.get_json()['ci'])
    if request.method == 'POST':
        result = userToReturn(mp.save())
    else:
        result = MedicalPersonnel.delete({'ci': mp.ci})

    return crudReturn(result)

@router.route('/doctor') # POST | DELETE /api/doctor
def doctor():
    d = Doctor(request.get_json()['ci'])
    if request.method == 'POST':
        result = userToReturn(d.save())
    else:
        result = Doctor.delete({'ci': d.ci})

    return crudReturn(result)

@router.route('/medicalAssistant') # POST | DELETE /api/medicalAssistant
def medicalAssitant():
    ma = MedicalAssitant(request.get_json()['ci'])
    if request.method == 'POST':
        result = userToReturn(ma.save())
    else:
        result = MedicalAssitant.delete({'ci': ma.ci})

    return crudReturn(result)

@router.route('/administrative') # POST | DELETE /api/administrative
def administrative():
    a = Administrative(request.get_json()['ci'])
    if request.method == 'POST':
        result = userToReturn(a.save())
    else:
        result = Administrative.delete({'ci': a.ci})

    return crudReturn(result)

@router.post('/surname1') # POST /api/user/surname1 filter by surname1 and userType
@router.get('/<surname1>') # GET /api/user/<surname1> filter only by surname1
def userBySurname1(surname1:str=None):
    if request.method == 'POST':
        conditionList = filterByType(request=request,dictReturn=True)
    else:
        conditionList = {'surname1' : surname1}

    return crudReturn([userToReturn(u) for u in User.filter(conditionList)])

@router.post('/name1surname1') # GET /api/user/name1surname1
@router.get('/<name1>/<surname1>') # GET /api/user/<name1>/<surname1>
def userByName1nSurname1(name1:str=None,surname1:str=None):
    if request.method == 'POST':
        conditionList = filterByType(request=request,dictReturn=True)
    else:
        conditionList = {'name1': name1, 'surname1' : surname1}

    return crudReturn([userToReturn(u) for u in User.filter(conditionList)])

@router.route('/phoneNumbers', methods=['POST', 'DELETE'])
@router.get('/phoneNumbers/<ci>')
def phoneNumbers(ci:int=None):
    result = None

    if request.method == 'GET':
        result = [asdict(p) for p in UserPhone.getByCi(ci)]
    else:
        data = request.get_json()['userPhone']
        for phone in data:
            if request.method == 'POST':
                UserPhone(**phone).save()
            elif request.method == 'DELETE':
                UserPhone.delete(phone)
        result = data if request.method == 'POST' else True

    return crudReturn(result)

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