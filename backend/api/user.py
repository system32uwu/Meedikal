import os
from flask import Blueprint, request
from dataclasses import asdict

from util.crud import crudReturn
from util.requestParsers import parseRole
from middleware.authGuard import requiresAuth, requiresRole

from middleware.data import passJsonData, passFile
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from models.Specialty import *
from models.User import *

router = Blueprint('user', __name__, url_prefix='/user')

def userToReturn(user: User, role=None):
    if user is None:
        return None
    if role is None:
        role = parseRole(request)
    
    obj = {'user': asdict(user), 
           'roles': User.getRoles(ci=user.ci),
           'phoneNumbers': [asdict(p) for p in UserPhone.getByCi(user.ci)]}

    if role == 'medicalPersonnel' or role == 'doctor' or role == 'medicalAssitant':
        hasSpec = MpHasSpec.filter({'ciMp': user.ci})
        obj['specialties'] = [asdict(hsp) for hsp in hasSpec]

        for hsp in obj['specialties']:
            hsp['title'] = Specialty.getById(hsp['idSpec']).title

    obj['user'].pop('password', None)

    return obj

@router.route('/all', methods=['GET', 'POST']) # GET | POST /api/user/all
@passJsonData
def allUsers(data:dict=None):
    return crudReturn([userToReturn(u) for u in User.filter(data)])

@router.get('/<int:ci>') # GET /api/user/<ci>
@router.post('/ci') # POST /api/user/ci
@passJsonData
def getUserByCi(ci:int=None, data:dict=None):
    if request.method == 'POST':
        ci = data['ci']

    return crudReturn(userToReturn(User.getByCi(ci)))

@router.post('') # POST /api/user
@requiresRole('administrative')
@passJsonData
def createUser(data:dict):
    return crudReturn(userToReturn(User(**data).save(data)))

@router.route('', methods=['PUT', 'PATCH']) # PUT | PATCH /api/user
@requiresAuth
@passJsonData
def updateUser(data:dict, ci:int):
    return crudReturn(User.updateByCi(ci, data))

@router.route('/<int:ci>', methods=['PUT', 'PATCH']) # PUT | PATCH /api/user
@requiresRole('administrative')
@passJsonData
def updateUserAsAdmin(data:dict):
    return crudReturn(User.updateByCi(data['ci'], data))

@router.delete('') # DELETE /api/user
@requiresRole('administrative')
@passJsonData
def deleteUser(data:dict):
    return crudReturn(User.delete(data))

@router.route('/photo', methods=['POST', 'PUT', 'PATCH'])
@requiresAuth
@passFile(['jpg', 'jpeg', 'png'])
def updatePhoto(ci:int, file:FileStorage):
    file.filename = secure_filename(f'{ci}.jpg') # force jpg format
    photoUrl = os.path.join(Config.UPLOAD_FOLDER, file.filename)
    file.save(photoUrl)
    User.getByCi(ci).update({'ci': ci, 'photoUrl': {"value": None, "newValue": photoUrl}})
    return crudReturn(file.filename)

@router.route('/patient', methods=['POST', 'DELETE']) # POST | DELETE /api/patient
@requiresRole('administrative')
@passJsonData
def patient(data:dict):
    if request.method == 'POST':
        result = userToReturn(Patient(**data).save(data))
    else:
        result = Patient.delete(data)

    return crudReturn(result)

@router.route('/medicalPersonnel', methods=['POST', 'DELETE']) # POST | DELETE /api/medicalPersonnel
@requiresRole('administrative')
@passJsonData
def medicalPersonnel(data:dict):
    if request.method == 'POST':
        result = userToReturn(MedicalPersonnel(**data).save(data))
    else:
        result = MedicalPersonnel.delete(data)

    return crudReturn(result)

@router.route('/doctor', methods=['POST', 'DELETE']) # POST | DELETE /api/doctor
@requiresRole('administrative')
@passJsonData
def doctor(data:dict):
    if request.method == 'POST':
        result = userToReturn(Doctor(**data).save(data))
    else:
        result = Doctor.delete(data)

    return crudReturn(result)

@router.route('/medicalAssistant', methods=['POST', 'DELETE']) # POST | DELETE /api/medicalAssistant
@requiresRole('administrative')
@passJsonData
def medicalAssitant(data:dict):
    if request.method == 'POST':
        result = userToReturn(MedicalAssitant(**data).save(data))
    else:
        result = MedicalAssitant.delete(data)

    return crudReturn(result)

@router.route('/administrative', methods=['POST', 'DELETE']) # POST | DELETE /api/administrative
@requiresRole('administrative')
@passJsonData
def administrative(data:dict):
    if request.method == 'POST':
        result = userToReturn(Administrative(**data).save(data))
    else:
        result = Administrative.delete(data)

    return crudReturn(result)

@router.get('/filter') # GET /api/user/filter filter with anything passed to the body of the request.
@passJsonData
def filterUser(data:dict):
    return crudReturn([userToReturn(u) for u in User.filter(data)])

@router.get('/<surname1>') # GET /api/user/<surname1> filter only by surname1
def userBySurname1(surname1:str=None):
    result = User.filter({'surname1' : surname1})
    return crudReturn([userToReturn(u) for u in result])

@router.get('/<name1>/<surname1>') # GET /api/user/<name1>/<surname1>
def userByName1nSurname1(name1:str=None, surname1:str=None):
    result = User.filter({'name1' : name1, 'surname1' : surname1})
    return crudReturn([userToReturn(u) for u in result])

def phoneNumbers(ci:int=None, data:dict=None):
    result = None

    if request.method == 'GET':
        result = UserPhone.getByCi(ci)
    else:
        data = data['userPhone']
        for phone in data:
            if request.method == 'POST':
                UserPhone(**phone).saveOrGet(phone)
            elif request.method == 'DELETE':
                rows = UserPhone.delete(phone)
        result = data if request.method == 'POST' else rows

    return crudReturn(result)

@router.get('/phoneNumbers/<int:ci>')
def getPhoneNumbers(ci:int, data:dict):
    return phoneNumbers(ci, data)

@router.route('/phoneNumbers', methods=['POST', 'DELETE'])
@requiresAuth
@passJsonData
def selfPhoneNumbers(ci:int, data:dict):
    return phoneNumbers(ci, data)

@router.route('/phoneNumbers/<int:ci>', methods=['POST', 'DELETE'])
@requiresRole('administrative')
@passJsonData
def phoneNumbersAsAdmin(ci:int, data:dict):
    return phoneNumbers(ci, data)

def mpHasSpec(ciMp:int=None, data:dict=None):
    if request.method == 'GET':
        result = MpHasSpec.filter({'ciMp': ciMp})
        for sp in result:
            sp['title'] = Specialty.getById(sp['idSpec']).title
    else:
        data = data['mpHasSpec']
        result = []
        for hsp in data:
            if request.method == 'POST':
                if hsp.get('idSpec', None) is None:
                    _sp = Specialty.saveOrGet({'title': hsp['title']}, returns='one')
                    hsp['idSpec'] = _sp.id
                    hsp.pop('title')
                
                hspInstance = MpHasSpec(**hsp).save(hsp)
                hspReturn = asdict(hspInstance)
                hspReturn['title'] = Specialty.getById(hsp['idSpec']).title
                result.append(hspReturn)

            elif request.method == 'DELETE':
                result = MpHasSpec.delete(hsp)

    return crudReturn(result)

@router.get('/medicalPersonnel/mpHasSpec/<int:ciMp>')
def getSpOfMp(ciMp:int):
    return mpHasSpec(ciMp=ciMp)

@router.route('/medicalPersonnel/mpHasSpec', methods=['POST', 'DELETE'])
@requiresRole('administrative') # only admin users can add or remove specialties of mp user
@passJsonData
def addOrDeleteMpHasSpec(data:dict):
    return mpHasSpec(data=data)

@router.get('/medicalPersonnel/<specialty>') # specialty title
@passJsonData
def filterMpUsersBySpecialty(specialty:str=None, data:dict=None):
    users = []
    baseConditions = {'specialty.title': specialty,
                      'mpHasSpec.ciMp': {
                        'value': 'medicalPersonnel.ci',
                        'joins': True},
                      'mpHasSpec.idSpec':{
                          'value': 'specialty.id',
                          'joins': True
                     }}

    if request.method == 'POST':
        mps:list[MedicalPersonnel] = MedicalPersonnel.filter(baseConditions | data)
    else:
        mps:list[MedicalPersonnel] = MedicalPersonnel.filter(baseConditions)
    
    users = [User.getByCi(mp.ci) for mp in mps]
            
    return crudReturn([userToReturn(u, 'medicalPersonnel') for u in users])