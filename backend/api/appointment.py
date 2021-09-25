from flask import Blueprint, request
from dataclasses import asdict

from models.Appointment import *
from models.ClinicalSign import ClinicalSign, RegistersCs
from models.Disease import Disease, Diagnoses
from models.Symptom import Symptom, RegistersSy
from util.crud import *
from util.returnMessages import *
from middleware.data import passJsonData

router = Blueprint('appointment', __name__, url_prefix='/appointment')

@router.get('/<int:id>') # GET /api/appointment/<id>
def getAppointmentById(id:int):
    return crudReturn(Appointment.getById(id))

@router.post('/filter') # POST /api/appointment/filter { 'name': 'oftalmology', 'state': 'OK', date: '2021-09-11', ... }
@passJsonData
def filterAppointments(data:dict):
    return crudReturn(Appointment.filter(data))

@router.post('') # POST /api/appointment
@passJsonData
def createAppointment(data:dict):
    return crudReturn(Appointment(**data).save(data))

@router.route('', methods=['PUT', 'PATCH']) # PUT | PATCH /api/appointment
@passJsonData
def updateAppointment(data:dict):
    return crudReturn(Appointment.update(data))

@router.delete('') # DELETE /api/appointment
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
@router.get('/assignedTo/<int:idAp>')
@router.get('/assignedTo/ciDoc/<int:ciDoc>')
@passJsonData
def assignedTo(idAp:int=None, ciDoc:int=None, data:dict=None): # a [doctor] is <assigned to> an [appointment]
    if request.method == 'GET':
        return getUserAppointment(AssignedTo, idAp, ciDoc, 'ciDoc')
    else:
        return operateUserAppointment(AssignedTo, data)

@router.route('/assistsAp', methods=['POST', 'PUT', 'PATCH', 'DELETE']) # POST | PUT | PATCH | DELETE /api/appointment/assistsAp
@router.get('/assistsAp/<int:idAp>')
@router.get('/assistsAp/ciMa/<int:ciMa>')
@passJsonData
def assistsAp(idAp:int=None,ciMa:int=None, data:dict=None): # a [medicalAssistant] <assists an> an [appointment]
    if request.method == 'GET':
        return getUserAppointment(AssistsAp, idAp, ciMa, 'ciMa')
    else:
        return operateUserAppointment(AssistsAp, data)
        
@router.route('/attendsTo', methods=['POST', 'PUT', 'PATCH', 'GET', 'DELETE']) # POST | PUT | PATCH | GET | DELETE /api/appointment/attendsTo
@router.get('/attendsTo/<int:idAp>')
@router.get('/attendsTo/ciPa/<int:ciPa>')
@passJsonData
def attendsTo(idAp:int=None,ciPa:int=None, data:dict=None): # a [patient] <attends to> an [appointment] 
    if request.method == 'GET':
        return getUserAppointment(AttendsTo, idAp, ciPa, 'ciPa')
    else:
        return operateUserAppointment(AttendsTo, data)
        
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
@router.get('/diagnoses/<int:idAp>/<int:ciPa>') # GET /api/appointment/diagnoses/<idAp>
@passJsonData
def diagnosedDisease(idAp:int=None, ciPa:int=None, data:dict=None): # input diagnosed diseases
    if request.method == 'GET':
        return getSufferingOfAp(Disease, Diagnoses, idAp, ciPa, 'idDis')
    else:
        return operateSufferingOfAp(Disease, Diagnoses, data, 'idDis')

@router.route('/registersSy', methods=['POST', 'DELETE']) # POST | DELETE /api/appointment/registersSy
@router.get('/registersSy/<int:idAp>/<int:ciPa>') # GET /api/appointment/registersSy/<idAp>
@passJsonData
def registersSy(idAp:int=None,ciPa:int=None, data:dict=None): # input registered symptoms
    if request.method == 'GET':
        return getSufferingOfAp(Symptom, RegistersSy, idAp, ciPa, 'idSy')
    else:
        return operateSufferingOfAp(Symptom, RegistersSy, data, 'idSy')

@router.route('/registersCs', methods=['POST', 'DELETE']) # POST | DELETE /api/appointment/registersCs
@router.get('/registersCs/<int:idAp>/<int:ciPa>') # GET /api/appointment/registersCs/<idAp>
@passJsonData
def registersCs(idAp:int=None, ciPa:int=None, data:dict=None): # input registered clinical signs
    if request.method == 'GET':
        return getSufferingOfAp(ClinicalSign, RegistersCs, idAp, ciPa, 'idCs')
    else:
        return operateSufferingOfAp(ClinicalSign, RegistersCs, data, 'idCs')