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

@router.route('/diagnoses', methods=['POST', 'DELETE']) # POST | DELETE /api/appointment/diagnoses
@router.get('/diagnoses/<int:idAp>/<int:ciPa>') # GET /api/appointment/diagnoses/<idAp>
@passJsonData
def diagnosedDisease(idAp:int=None, ciPa:int=None, data:dict=None): # input diagnosed diseases
    if request.method == 'GET':
        result = Diagnoses.filter({'idAp': idAp, 'ciPa': ciPa})
        for d in result:
            d['name'] = Disease.getById(d['idDis']).name
    else:
        data = data['diagnoses']
        result = []

        for d in data:
            if request.method == 'POST':
                if d.get('idDis', None) is None:
                    _d = Disease.saveOrGet({'name': d['name']})
                    d['idDis'] = _d.id
                    d.pop('name')

                diagnosesInstance = Diagnoses(**d).save(d)
                diagnosesReturn = asdict(diagnosesInstance)
                diagnosesReturn['name'] = Disease.getById(d['idDis']).name
                result.append(diagnosesReturn)

            elif request.method == 'DELETE':
                result.append(Diagnoses.delete(d))

    return crudReturn(result)

@router.route('/registersSy', methods=['POST', 'DELETE']) # POST | DELETE /api/appointment/registersSy
@router.get('/registersSy/<int:idAp>/<int:ciPa>') # GET /api/appointment/registersSy/<idAp>
@passJsonData
def registersSy(idAp:int=None,ciPa:int=None, data:dict=None): # input registered symptoms
    if request.method == 'GET':
        result = RegistersSy.filter({'idAp': idAp,'ciPa': ciPa})
        for sy in result:
            sy['name'] = Symptom.getById(sy['idSy']).name
    else:
        data = data['registersSy']
        result = []

        for s in data:
            if request.method == 'POST':
                if s.get('idSy', None) is None:
                    _s = Symptom.saveOrGet({'name': s['name']})
                    s['idSy'] = _s.id
                    s.pop('name')

                registersSyInstance = RegistersSy(**s).save(s)
                registersSyReturn = asdict(registersSyInstance)
                registersSyReturn['name'] = Symptom.getById(s['idSy']).name
                result.append(registersSyReturn)

            elif request.method == 'DELETE':
                result.append(RegistersSy.delete(s))

    return crudReturn(result)

@router.route('/registersCs', methods=['POST', 'DELETE']) # POST | DELETE /api/appointment/registersCs
@router.get('/registersCs/<int:idAp>/<int:ciPa>') # GET /api/appointment/registersCs/<idAp>
@passJsonData
def registersCs(idAp:int=None, ciPa:int=None, data:dict=None): # input registered clinical signs
    if request.method == 'GET':
        result = RegistersCs.filter({'idAp': idAp, 'ciPa': ciPa})
        for cs in result:
            cs['name'] = ClinicalSign.getById(cs['idCs']).name
    else:
        data = data['registersCs']
        result = []

        for cs in data:
            if request.method == 'POST':
                if cs.get('idCs', None) is None:
                    _cs = ClinicalSign.saveOrGet({'name': cs['name']})
                    cs['idCs'] = _cs.id
                    cs.pop('name')
                
                registersCsInstance = RegistersCs(**cs).save(cs)
                registersCsReturn = asdict(registersCsInstance)
                registersCsReturn['name'] = ClinicalSign.getById(cs['idCs']).name
                result.append(registersCsReturn)

            elif request.method == 'DELETE':
                result.append(RegistersCs.delete(cs))

    return crudReturn(result)