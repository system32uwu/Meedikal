from dataclasses import asdict

from flask import jsonify, Blueprint, request, Request

from models.Specialty import *
from models.User import *
from util.returnMessages import *

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

    phones = UserPhone.getByCi(user.ci)

    obj = {'user': asdict(user), 
           'types': getTypes(user.ci)}

    if phones is not None:
        obj['phoneNumbers'] = [asdict(p) for p in phones]

    if userType == 'medicalPersonnel' or userType == 'doctor' or userType == 'medicalAssitant':
        hasSpec = MpHasSpec.query({'ciMp': user.ci})
        obj['specialties'] = [asdict(Specialty.filter({'id': id})) for id in 
                             [sp for sp in hasSpec]]

    obj['user'].pop('password', None)

    return obj

@router.get('/all') # GET /api/user/all
def allUsers():
    users = filterByType(request=request)
    return jsonify({"result": [userToReturn(u) for u in users]}), 200
    # return jsonify([userToReturn(u) for u in users]), 200
    # return crudv2(request=request, preparedResult=[userToReturn(u) for u in users])

# @router.get('') # GET /api/user
# def user():
#     data = json.loads(request.data)
    
#     if data.get('password', None) is not None: # encrypt the password
#         data['password'] = generate_password_hash(data['password'])

#     request.data = json.dumps({User.__tablename__: data})
#     return crudv2(User,request)
    
# @router.delete('') # DELETE /api/user
# def deleteUser(): # logicalCD (logical Create / Delete) = set active to False or True (0,1)
#     data = json.loads(request.data)['user']
#     user = filterByType(request=request).filter(User.ci == data['ci']).one_or_none()
#     if data.get('logicalCD', None) is not None:
#         if user is not None:
#             user.active = data['logicalCD']
#             user.update()
#             return crudv2(request=request,preparedResult=userToReturn(user))
#     else:
#         return crudv2(User,request)

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