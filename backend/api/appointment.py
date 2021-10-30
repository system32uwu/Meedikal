from flask import Blueprint, request
from dataclasses import asdict

from models.User import Doctor, User
from models.Appointment import *
from models.Branch import Branch
from models.ClinicalSign import ClinicalSign, RegistersCs
from models.Disease import Disease, Diagnoses
from models.Symptom import Symptom, RegistersSy
from util.crud import *
from util.returnMessages import *
from middleware.authGuard import requiresRole, requiresAuth
from middleware.data import passJsonData, paginated
from models import db
from .user import userToReturn

router = Blueprint('appointment', __name__, url_prefix='/appointment')

@router.route('/all', methods=['GET', 'POST'])
@requiresAuth
@paginated()
def all(offset:int, limit:int, data:dict=None, **kwargs):
    return crudReturn(Appointment.filter(data, offset=offset, limit=limit))

@router.get('/<int:id>') # GET /api/appointment/<id>
@requiresAuth
def getAppointmentById(id:int, **kwargs):
    return crudReturn(Appointment.getById(id))

@router.post('') # POST /api/appointment
@requiresRole(['administrative'])
@passJsonData
def createAppointment(data:dict):
    return crudReturn(Appointment(**data).save(data))

@router.route('', methods=['PUT', 'PATCH']) # PUT | PATCH /api/appointment
@requiresRole(['administrative'])
@passJsonData
def updateAppointment(data:dict):
    return crudReturn(Appointment.update(data))

@router.route('/<int:id>', methods=['PUT', 'PATCH']) # PUT | PATCH /api/appointment/id
@requiresRole(['administrative'])
@passJsonData
def updateAppointmentById(id:int, data:dict, **kw):
    return crudReturn(Appointment.updateById(id, data))

@router.delete('') # DELETE /api/appointment
@requiresRole(['administrative'])
@passJsonData
def deleteAppointment(data:dict):
    return crudReturn(Appointment.delete(data))

# -- Users <> appointment

def getUserAppointment(relationship:BaseModel, idAp:int, ciUser:int, ciField:str):
    conditions = {}
    if idAp is not None:
        conditions['idAp'] = idAp
    if ciUser is not None:
        conditions[ciField] = ciUser
    return crudReturn(relationship.filter(conditions))

def operateUserAppointment(relationship:BaseModel, data:dict):
    if request.method == 'POST':
        return crudReturn(relationship(**data).save(data))
    elif request.method == 'PUT' or request.method == 'PATCH':
        print(data)
        return crudReturn(relationship.update(data))
    elif request.method == 'DELETE':
        return crudReturn(relationship.delete(data))

@router.route('/assignedTo', methods=['POST', 'PUT', 'PATCH', 'DELETE']) # POST | PUT | PATCH | DELETE /api/appointment/assignedTo
@requiresRole(['administrative'])
@passJsonData
def operateAssignedTo(data:dict):
    return operateUserAppointment(AssignedTo, data)

@router.get('/assignedTo/<int:idAp>')
@router.get('/assignedTo/ciDoc/<int:ciDoc>')
@requiresAuth
@paginated()
def getAssignedTo(idAp:int=None, ciDoc:int=None, **kwargs): # a [doctor] is <assigned to> an [appointment]
    return getUserAppointment(AssignedTo, idAp, ciDoc, 'ciDoc')
        
@router.route('/attendsTo', methods=['POST', 'PUT', 'PATCH', 'GET', 'DELETE']) # POST | PUT | PATCH | GET | DELETE /api/appointment/attendsTo
@requiresRole(['administrative', 'patient', 'doctor'])
@passJsonData
def operateAttendsTo(data:dict):
    # TODO: -1: if it's patient making the appointment, ensure that the ci provided body is equal to the logged in patient
    return operateUserAppointment(AttendsTo, data)

@router.get('/attendsTo/<int:idAp>')
@router.get('/attendsTo/ciPa/<int:ciPa>')
@requiresAuth
@paginated()
def getAttendsTo(idAp:int=None, ciPa:int=None, **kwargs): # a [patient] <attends to> an [appointment] 
    return getUserAppointment(AttendsTo, idAp, ciPa, 'ciPa')
        
# # -- DATA INPUTTED WHEN A PATIENT IS BEING INTERVIEWED IN AN APPOINTMENT

def getSufferingOfAp(entity:BaseModel, relationship:BaseModel, idAp:int, ciPa:int, idField:str, nameField:str='name'):
    result = [asdict(r) for r in relationship.filter({'idAp': idAp, 'ciPa': ciPa})]
    for row in result:
        row[nameField] = asdict(entity.getById(row[idField]))[nameField]
    return crudReturn(result)

def operateSufferingOfAp(entity:BaseModel, relationship:BaseModel, data:dict, idField:str, nameField:str='name'):
    result = []
    for row in data[relationship.__tablename__]:
        if row.get(idField, None) is None:
            _entity = entity.saveOrGet({nameField: row[nameField]}, returns='one')
            row[idField] = _entity.id
            row.pop(nameField)

        if request.method == 'POST':
            relationshipInstance = relationship(**row).save(row)
            relationshipReturn = asdict(relationshipInstance)
            relationshipReturn[nameField] = asdict(entity.getById(row[idField]))[nameField]
            result.append(relationshipReturn)

        elif request.method == 'DELETE':
            result.append(relationship.delete(row))

    return crudReturn(result)

@router.route('/diagnoses', methods=['POST', 'DELETE']) # POST | DELETE /api/appointment/diagnoses
@requiresRole(['doctor'])
@passJsonData
def operateDiagnose(data:dict):
    return operateSufferingOfAp(Disease, Diagnoses, data, 'idDis')

@router.get('/diagnoses/<int:idAp>/<int:ciPa>') # GET /api/appointment/diagnoses/<idAp>
@requiresAuth
def getDiagnosed(idAp:int=None, ciPa:int=None, **kwargs): # get diagnosed diseases
    return getSufferingOfAp(Disease, Diagnoses, idAp, ciPa, 'idDis')

@router.route('/registersSy', methods=['POST', 'DELETE']) # POST | DELETE /api/appointment/registersSy
@requiresRole(['doctor'])
@passJsonData
def operateRegistersSy(data:dict):
    return operateSufferingOfAp(Symptom, RegistersSy, data, 'idSy')

@router.get('/registersSy/<int:idAp>/<int:ciPa>') # GET /api/appointment/registersSy/<idAp>
@requiresAuth
def getRegisteredSy(idAp:int=None,ciPa:int=None, **kwargs): # get registered symptoms
    return getSufferingOfAp(Symptom, RegistersSy, idAp, ciPa, 'idSy')

@router.route('/registersCs', methods=['POST', 'DELETE']) # POST | DELETE /api/appointment/registersCs
@requiresRole(['doctor'])
@passJsonData
def operateRegistersCs(data:dict):
    return operateSufferingOfAp(ClinicalSign, RegistersCs, data, 'idCs')

@router.get('/registersCs/<int:idAp>/<int:ciPa>') # GET /api/appointment/registersCs/<idAp>
@requiresAuth
def getRegisteredCs(idAp:int=None, ciPa:int=None, **kwargs): # input registered clinical signs
    return getSufferingOfAp(ClinicalSign, RegistersCs, idAp, ciPa, 'idCs')

@router.post('/filter')
@requiresAuth
@paginated()
def filterAps(ci:int, offset:int, limit:int, data:dict={}, **kwargs): # return appointment, doctor and branch
    _selectedDate = data['selectedDate']
    _from = data['timeInterval']['from']
    _to = data['timeInterval']['to']
    _timeFilter = data['timeFilter']
    _typeFilter = data['typeFilter']
    _doctorSurname1 = data.get('doctorSurname1', None)
    _appointmentName = data.get('appointmentName', None)

    tables = ['appointment']
    conditions = []
    values = []

    if _timeFilter == 'selectedDay' or _timeFilter == 'selectedMonth':
        conditions.append('appointment.date >= ? and appointment.date <= ?') # ?1: _from, ?2: _to
        values.append(_from)
        values.append(_to)
    elif _timeFilter == 'future':
        conditions.append('appointment.date >= ?') # ?1: _selectedDate
        values.append(_selectedDate)
    elif _timeFilter == 'past':
        conditions.append('appointment.date <= ?') # ?1: _selectedDate
        values.append(_selectedDate)

    if _appointmentName:
        conditions.append("appointment.name LIKE ?")
        values.append(_appointmentName)
    
    if _typeFilter == 'mine':
        conditions.append('attendsTo.ciPa = ?') 
        conditions.append('attendsTo.idAp = appointment.id') 
        tables.append('attendsTo')
        values.append(ci)
    if _typeFilter == 'mine-doctor':
        conditions.append('assignedTo.ciDoc = ?')
        conditions.append('assignedTo.idAp = appointment.id')
        tables.append('assignedTo')
        values.append(ci)

    if _doctorSurname1:
        conditions.append("user.surname1 LIKE ?")
        conditions.append("user.ci = doctor.ci")
        conditions.append('assignedTo.ciDoc = doctor.ci')
        conditions.append('assignedTo.idAp = appointment.id')
        tables.append('assignedTo')
        tables.append('doctor')
        tables.append('user')
        values.append(_doctorSurname1)

    statementData = f"""
    SELECT appointment.* FROM {', '.join(tables)}
    {' WHERE ' + ' AND '.join(conditions) if len(conditions) > 0 else ''}
    LIMIT {limit} OFFSET {offset}
    """
    print(statementData,values)
    statementCount = f"""
    SELECT COUNT(appointment.id) FROM {', '.join(tables)}
    {' WHERE ' + ' AND '.join(conditions) if len(conditions) > 0 else ''}
    """

    resultData = [{'appointment': asdict(Appointment(*ap))} for ap in db.execute(statementData, values).fetchall()]

    resultCount = db.execute(statementCount, values).fetchone()[0]
    
    for r in resultData:
        doc = Doctor.getDocOfAp(r['appointment']['id'])
        br = Branch.getBranchOfAp(r['appointment']['id'])

        if isinstance(doc, User):
            r['doctor'] = userToReturn(doc)
        else:
            r['doctor'] = {}

        if isinstance(br, Branch):
            r['branch'] = asdict(br)
        else:
            r['branch'] = {}

        patients = AttendsTo.getPatients(r['appointment']['id']) or []
        if len(patients) > 0:
            r['patients'] = [asdict(p) for p in patients]
        else:
            r['patients'] = []

    return crudReturn(resultData, {'total': resultCount})