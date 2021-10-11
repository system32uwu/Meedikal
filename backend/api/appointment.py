from flask import Blueprint, request
from dataclasses import asdict

from models.Appointment import *
from models.ClinicalSign import ClinicalSign, RegistersCs
from models.Disease import Disease, Diagnoses
from models.Symptom import Symptom, RegistersSy
from util.crud import *
from util.returnMessages import *
from middleware.authGuard import requiresRole
from middleware.data import passJsonData

router = Blueprint('appointment', __name__, url_prefix='/appointment')

@router.get('/<int:id>') # GET /api/appointment/<id>
def getAppointmentById(id:int):
    return crudReturn(Appointment.getById(id))

@router.get('/filter') # GET /api/appointment/filter filter  with anything passed to the body of the request.
@passJsonData
def filterAppointments(data:dict):
    return crudReturn(Appointment.filter(data))

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
@passJsonData
def getAssignedTo(idAp:int=None, ciDoc:int=None): # a [doctor] is <assigned to> an [appointment]
    return getUserAppointment(AssignedTo, idAp, ciDoc, 'ciDoc')

@router.route('/assistsAp', methods=['POST', 'PUT', 'PATCH', 'DELETE']) # POST | PUT | PATCH | DELETE /api/appointment/assistsAp
@requiresRole(['administrative'])
@passJsonData
def operateAssistsAp(data:dict):
    return operateUserAppointment(AssistsAp, data)

@router.get('/assistsAp/<int:idAp>')
@router.get('/assistsAp/ciMa/<int:ciMa>')
def getAssistsAp(idAp:int=None,ciMa:int=None): # a [medicalAssistant] <assists an> an [appointment]
    return getUserAppointment(AssistsAp, idAp, ciMa, 'ciMa')
        
@router.route('/attendsTo', methods=['POST', 'PUT', 'PATCH', 'GET', 'DELETE']) # POST | PUT | PATCH | GET | DELETE /api/appointment/attendsTo
@requiresRole(['administrative', 'patient'])
@passJsonData
def operateAttendsTo(data:dict):
    # TODO: -1: if it's patient making the appointment, ensure that the ci provided body is equal to the logged in patient
    # TODO: -2: validate the number and/or the time (number shouldn't be present in any other row that has the same idAp) 
    return operateUserAppointment(AttendsTo, data)

@router.get('/attendsTo/<int:idAp>')
@router.get('/attendsTo/ciPa/<int:ciPa>')
def getAttendsTo(idAp:int=None,ciPa:int=None): # a [patient] <attends to> an [appointment] 
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
        if request.method == 'POST':
            if row.get(idField, None) is None:
                _entity = entity.saveOrGet({nameField: row[nameField]}, returns='one')
                row[idField] = _entity.id
                row.pop(nameField)
                            
            relationshipInstance = relationship(**row).save(row)
            relationshipReturn = asdict(relationshipInstance)
            relationshipReturn[nameField] = asdict(entity.getById(row[idField]))[nameField]
            result.append(relationshipReturn)

        elif request.method == 'DELETE':
            result.append(relationship.delete(row))

    return crudReturn(result)

@router.route('/diagnoses', methods=['POST', 'DELETE']) # POST | DELETE /api/appointment/diagnoses
@requiresRole(['medicalPersonnel'])
@passJsonData
def operateDiagnose(data:dict):
    return operateSufferingOfAp(Disease, Diagnoses, data, 'idDis')

@router.get('/diagnoses/<int:idAp>/<int:ciPa>') # GET /api/appointment/diagnoses/<idAp>
def getDiagnosed(idAp:int=None, ciPa:int=None): # input diagnosed diseases
    return getSufferingOfAp(Disease, Diagnoses, idAp, ciPa, 'idDis')

@router.route('/registersSy', methods=['POST', 'DELETE']) # POST | DELETE /api/appointment/registersSy
@requiresRole(['medicalPersonnel'])
@passJsonData
def operateRegistersSy(data:dict):
    return operateSufferingOfAp(Symptom, RegistersSy, data, 'idSy')

@router.get('/registersSy/<int:idAp>/<int:ciPa>') # GET /api/appointment/registersSy/<idAp>
def getRegisteredSy(idAp:int=None,ciPa:int=None, data:dict=None): # input registered symptoms
    return getSufferingOfAp(Symptom, RegistersSy, idAp, ciPa, 'idSy')

@router.route('/registersCs', methods=['POST', 'DELETE']) # POST | DELETE /api/appointment/registersCs
@requiresRole(['medicalPersonnel'])
@passJsonData
def operateRegistersCs(data:dict):
    return operateSufferingOfAp(ClinicalSign, RegistersCs, data, 'idCs')

@router.get('/registersCs/<int:idAp>/<int:ciPa>') # GET /api/appointment/registersCs/<idAp>
def getRegisteredCs(idAp:int=None, ciPa:int=None): # input registered clinical signs
    return getSufferingOfAp(ClinicalSign, RegistersCs, idAp, ciPa, 'idCs')