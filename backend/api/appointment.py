from dataclasses import asdict
from models.Appointment import *
from models.ClinicalSign import ClinicalSign, RegistersCs
from models.Disease import Disease, Diagnoses
from models.Symptom import Symptom, RegistersSy
from flask import Blueprint, request

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

@router.route('/assignedTo', methods=['POST', 'PUT', 'PATCH', 'DELETE']) # POST | PUT | PATCH | DELETE /api/appointment/assignedTo
@router.get('/assignedTo/<int:idAp>')
@router.get('/assignedTo/ciDoc/<int:ciDoc>')
@passJsonData
def assignedTo(idAp:int=None, ciDoc:int=None, data:dict=None): # a [doctor] is <assigned to> an [appointment]
    if request.method == 'GET':
        conditions = {}
        if idAp is not None:
            conditions['idAp'] = idAp
        if ciDoc is not None:
            conditions['ciDoc'] = ciDoc
        return crudReturn(AssignedTo.filter(conditions))
    else:
        if request.method == 'POST':
            return crudReturn(AssignedTo(**data).save(data))
        if request.method == 'PUT' or request.method == 'PATCH':
            return crudReturn(AssignedTo.update(data))
        if request.method == 'DELETE':
            return crudReturn(AssignedTo.delete(data))
    
@router.route('/assistsAp', methods=['POST', 'PUT', 'PATCH', 'DELETE']) # POST | PUT | PATCH | DELETE /api/appointment/assistsAp
@router.get('/assistsAp/<int:idAp>')
@router.get('/assistsAp/ciMa/<int:ciMa>')
@passJsonData
def assistsAp(idAp:int=None,ciMa:int=None, data:dict=None): # a [medicalAssistant] <assists an> an [appointment]
    if request.method == 'GET':
        conditions = {}
        if idAp is not None:
            conditions['idAp'] = idAp
        if ciMa is not None:
            conditions['ciMa'] = ciMa
        return crudReturn(AssistsAp.filter(conditions))
    else:
        if request.method == 'POST':
            return crudReturn(AssistsAp(**data).save(data))
        if request.method == 'PUT' or request.method == 'PATCH':
            return crudReturn(AssistsAp.update(data))
        if request.method == 'DELETE':
            return crudReturn(AssistsAp.delete(data))
        
@router.route('/attendsTo', methods=['POST', 'PUT', 'PATCH', 'GET', 'DELETE']) # POST | PUT | PATCH | GET | DELETE /api/appointment/attendsTo
@router.get('/attendsTo/<int:idAp>')
@router.get('/attendsTo/ciPa/<int:ciPa>')
@passJsonData
def attendsTo(idAp:int=None,ciPa:int=None, data:dict=None): # a [patient] <attends to> an [appointment] 
    if request.method == 'GET':
        conditions = {}
        if idAp is not None:
            conditions['idAp'] = idAp
        if ciPa is not None:
            conditions['ciPa'] = ciPa
        return crudReturn(AttendsTo.filter(conditions))
    else:
        if request.method == 'POST':
            return crudReturn(AttendsTo(**data).save(data))
        if request.method == 'PUT' or request.method == 'PATCH':
            return crudReturn(AttendsTo.update(data))
        if request.method == 'DELETE':
            return crudReturn(AttendsTo.delete(data))
        
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