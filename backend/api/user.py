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
    result = User.save(request.get_json())
    return crudReturn(userToReturn(result, request=request))

@router.route('', methods=['PUT', 'PATCH']) # PUT | PATCH /api/user
def updateUser():
    result = User.update(request.get_json())
    return crudReturn([userToReturn(u) for u in result])

@router.delete('') # DELETE /api/user
def deleteUser():
    result = User.delete(request.get_json())
    return crudReturn(result)

@router.route('/patient', methods=['POST', 'DELETE']) # POST | DELETE /api/patient
def patient():
    if request.method == 'POST':
        result = userToReturn(Patient.save(request.get_json()))
    else:
        result = Patient.delete(request.get_json())

    return crudReturn(result)

@router.route('/medicalPersonnel', methods=['POST', 'DELETE']) # POST | DELETE /api/medicalPersonnel
def medicalPersonnel():
    if request.method == 'POST':
        result = userToReturn(MedicalPersonnel.save(request.get_json()))
    else:
        result = MedicalPersonnel.delete(request.get_json())

    return crudReturn(result)

@router.route('/doctor', methods=['POST', 'DELETE']) # POST | DELETE /api/doctor
def doctor():
    if request.method == 'POST':
        result = userToReturn(Doctor.save(request.get_json()))
    else:
        result = Doctor.delete(request.get_json())

    return crudReturn(result)

@router.route('/medicalAssistant', methods=['POST', 'DELETE']) # POST | DELETE /api/medicalAssistant
def medicalAssitant():
    if request.method == 'POST':
        result = userToReturn(MedicalAssitant.save(request.get_json()))
    else:
        result = MedicalAssitant.delete(request.get_json())

    return crudReturn(result)

@router.route('/administrative', methods=['POST', 'DELETE']) # POST | DELETE /api/administrative
def administrative():
    if request.method == 'POST':
        result = userToReturn(Administrative.save(request.get_json()))
    else:
        result = Administrative.delete(request.get_json())

    return crudReturn(result)

@router.post('/surname1') # POST /api/user/surname1 filter by surname1 and userType
@router.get('/<surname1>') # GET /api/user/<surname1> filter only by surname1
def userBySurname1(surname1:str=None):
    if request.method == 'POST':
        result = User.filter(request.get_json())
    else:
        result = User.filter({'surname1' : surname1})

    return crudReturn([userToReturn(u, request=request) for u in result])

@router.post('/name1surname1') # GET /api/user/name1surname1
@router.get('/<name1>/<surname1>') # GET /api/user/<name1>/<surname1>
def userByName1nSurname1(name1:str=None,surname1:str=None):
    if request.method == 'POST':
        result = User.filter(request.get_json())
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
                UserPhone.saveOrGet(phone)
            elif request.method == 'DELETE':
                rows = UserPhone.delete(phone)
        result = data if request.method == 'POST' else rows

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
                    _sp = Specialty.saveOrGet({'title': hsp['title']})
                    hsp['idSpec'] = _sp.id
                    hsp.pop('title')
                
                hspInstance = MpHasSpec.save(hsp)
                hspReturn = asdict(hspInstance)
                hspReturn['title'] = Specialty.getById(hsp['idSpec']).title
                result.append(hspReturn)

            elif request.method == 'DELETE':
                result = MpHasSpec.delete(hsp)

    return crudReturn(result)

@router.post('/medicalPersonnel/specialty') # {'title': 'oftalmology', 'extraFilters': {'userType': 'doctor'}}
@router.get('/medicalPersonnel/<title>') # specialty title
def getMpUsersBySpecialty(title:str=None):
    if request.method == 'POST':
        users = MedicalPersonnel.getBySpecialty(request=request)
    else:
        users = MedicalPersonnel.getBySpecialty(title=title)
    return crudReturn([userToReturn(u, 'medicalPersonnel') for u in users])