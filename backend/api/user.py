from werkzeug.security import generate_password_hash
from util.crud import crudReturn
from util.requestParsers import parseUserType
from middleware.authGuard import requiresAuth
from dataclasses import asdict

from flask import Blueprint, json, request

from models.Specialty import *
from models.User import *

router = Blueprint('user', __name__, url_prefix='/user')

def userToReturn(user: User, userType=None, request:Request=None):
    if user is None:
        return None
    if request is not None:
        userType = parseUserType(request)
    
    obj = {'user': asdict(user), 
           'roles': User.getRoles(ci=user.ci),
           'phoneNumbers': [asdict(p) for p in UserPhone.getByCi(user.ci)]}

    if userType == 'medicalPersonnel' or userType == 'doctor' or userType == 'medicalAssitant':
        hasSpec = MpHasSpec.filter({'ciMp': user.ci})
        obj['specialties'] = [asdict(hsp) for hsp in hasSpec]

    obj['user'].pop('password', None)
    
    return obj

@router.route('/all', methods=['GET', 'POST']) # GET | POST /api/user/all
def allUsers():
    users = User.filter(request.get_json())
    return crudReturn([userToReturn(u, request=request) for u in users])

@router.get('/<int:ci>') # GET /api/user/<ci>
@router.post('/ci') # POST /api/user/ci
def getUserByCi(ci:int=None):
    if request.method == 'POST':
        ci = request.get_json()['ci']

    u = User.getByCi(ci)
    return crudReturn(userToReturn(u, request=request))

@router.post('') # POST /api/user
def createUser():
    data = json.loads(request.data)
    
    data['password'] = generate_password_hash(data['password'])

    result = User.save(data)

    return crudReturn(userToReturn(result, request=request))

@router.route('', methods=['PUT', 'PATCH']) # PUT | PATCH /api/user
def updateUser():
    data = json.loads(request.data)
    
    if data.get('password', None) is not None: # encrypt the password
        if data['password'].get('value', None) is not None:
            data['password']['value'] = generate_password_hash(data['password']['value'])
        if data['password'].get('newValue', None) is not None:
            data['password']['newValue'] = generate_password_hash(data['password']['newValue'])

    result = User.update(data)
    return crudReturn([userToReturn(u) for u in result])

@router.delete('') # DELETE /api/user
def deleteUser():
    result = User.delete(request.get_json())
    return crudReturn(result)

@router.route('/patient', methods=['POST', 'DELETE']) # POST | DELETE /api/patient
def patient():
    p = Patient(request.get_json()['ci'])
    if request.method == 'POST':
        result = userToReturn(p.save())
    else:
        result = Patient.delete({'ci': p.ci})

    return crudReturn(result)

@router.route('/medicalPersonnel', methods=['POST', 'DELETE']) # POST | DELETE /api/medicalPersonnel
def medicalPersonnel():
    mp = MedicalPersonnel(request.get_json()['ci'])
    if request.method == 'POST':
        result = userToReturn(mp.save())
    else:
        result = MedicalPersonnel.delete({'ci': mp.ci})

    return crudReturn(result)

@router.route('/doctor', methods=['POST', 'DELETE']) # POST | DELETE /api/doctor
def doctor():
    d = Doctor(request.get_json()['ci'])
    if request.method == 'POST':
        result = userToReturn(d.save())
    else:
        result = Doctor.delete({'ci': d.ci})

    return crudReturn(result)

@router.route('/medicalAssistant', methods=['POST', 'DELETE']) # POST | DELETE /api/medicalAssistant
def medicalAssitant():
    ma = MedicalAssitant(request.get_json()['ci'])
    if request.method == 'POST':
        result = userToReturn(ma.save())
    else:
        result = MedicalAssitant.delete({'ci': ma.ci})

    return crudReturn(result)

@router.route('/administrative', methods=['POST', 'DELETE']) # POST | DELETE /api/administrative
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
        result = User.getByType(request=request)
    else:
        result = User.filter({'surname1' : surname1})

    return crudReturn([userToReturn(u, request=request) for u in result])

@router.post('/name1surname1') # GET /api/user/name1surname1
@router.get('/<name1>/<surname1>') # GET /api/user/<name1>/<surname1>
def userByName1nSurname1(name1:str=None,surname1:str=None):
    if request.method == 'POST':
        result = User.getByType(request=request)
    else:
        result = User.filter({'name1' : name1,'surname1' : surname1})

    return crudReturn([userToReturn(u, request=request) for u in result])

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

@router.route('/medicalPersonnel/mpHasSpec', methods=['POST', 'DELETE'])
@router.get('/medicalPersonnel/mpHasSpec/<int:ciMp>')
def mpHasSpec(ciMp:int=None):
    if request.method == 'GET':
        result = [asdict(sp) for sp in MpHasSpec.filter({'ciMp': ciMp})]
        for sp in result:
            sp['title'] = Specialty.getById(sp['idSpec']).title
    else:
        data = request.get_json()['mpHasSpec']
        result = []
        for hsp in data:
            if request.method == 'POST':
                if hsp.get('idSpec', None) is None:
                    _sp = Specialty(title=hsp['title']).saveOrGet(['title'])
                    hsp['idSpec'] = _sp.id
                    hsp.pop('title')
                
                hspInstance = MpHasSpec(**hsp).save()
                hspReturn = asdict(hspInstance)
                hspReturn['title'] = Specialty.getById(hsp['idSpec']).title
                result.append(hspReturn)

            elif request.method == 'DELETE':
                MpHasSpec.delete(hsp)
                result = True

    return crudReturn(result)

@router.post('/medicalPersonnel/specialty') # {'title': 'oftalmology', 'extraFilters': {'userType': 'doctor'}}
@router.get('/medicalPersonnel/<title>') # specialty title
def getMpUsersBySpecialty(title:str=None):
    if request.method == 'POST':
        users = MedicalPersonnel.getBySpecialty(request=request)
    else:
        users = MedicalPersonnel.getBySpecialty(title=title)
    return crudReturn([userToReturn(u, 'medicalPersonnel') for u in users])