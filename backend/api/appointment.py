from dataclasses import asdict

from models.ClinicalSign import ClinicalSign, RegistersCs
from models.Disease import Disease, Diagnoses
from models.Symptom import Symptom, RegistersSy
from flask import Blueprint, request

from util.crud import *
from util.returnMessages import *

from models.Appointment import *

router = Blueprint('appointment', __name__, url_prefix='/appointment')

@router.get('/<int:id>') # GET /api/appointment/<id>
def getAppointmentById(id:int):
    a = Appointment.getById(id)
    print(a)
    return crudReturn(asdict(a))

@router.post('/filter') # POST /api/appointment/filter { 'name': 'oftalmology', 'state': 'OK', date: '2021-09-11', ... }
def filterAppointments():
    aps = Appointment.filter(request.get_json())
    return crudReturn([asdict(ap) for ap in aps])

@router.post('') # POST /api/appointment
def createAppointment():
    a = Appointment(**request.get_json()).save()
    print(a)
    return crudReturn(asdict(a))

@router.route('', methods=['PUT', 'PATCH']) # PUT | PATCH /api/appointment
def updateAppointment():
    aps = Appointment.update(request.get_json())
    return crudReturn([asdict(ap) for ap in aps])

@router.delete('') # DELETE /api/appointment
def deleteAppointment():
    a = Appointment.delete(request.get_json())
    return crudReturn(a)

@router.route('/assignedTo', methods=['POST', 'PUT', 'PATCH', 'DELETE']) # POST | PUT | PATCH | DELETE /api/appointment/assignedTo
@router.get('/assignedTo/<int:idAp>')
@router.get('/assignedTo/ciDoc/<int:ciDoc>')
def assignedTo(idAp:int=None, ciDoc:int=None): # a [doctor] is <assigned to> an [appointment]
    if request.method == 'GET':
        conditions = {}
        if idAp is not None:
            conditions['idAp'] = idAp
        if ciDoc is not None:
            conditions['ciDoc'] = ciDoc
        return crudReturn([asdict(ast) for ast in AssignedTo.filter(conditions)])
    else:
        data = request.get_json()
        if request.method == 'POST':
            return crudReturn(asdict(AssignedTo(**data).save()))
        if request.method == 'PUT' or request.method == 'PATCH':
            return crudReturn([asdict(ast) for ast in AssignedTo.update(data)])
        if request.method == 'DELETE':
            return crudReturn(AssignedTo.delete(data))
    
@router.route('/assistsAp', methods=['POST', 'PUT', 'PATCH', 'DELETE']) # POST | PUT | PATCH | DELETE /api/appointment/assistsAp
@router.get('/assistsAp/<int:idAp>')
@router.get('/assistsAp/ciMa/<int:ciMa>')
def assistsAp(idAp:int=None,ciMa:int=None): # a [medicalAssistant] <assists an> an [appointment]
    if request.method == 'GET':
        conditions = {}
        if idAp is not None:
            conditions['idAp'] = idAp
        if ciMa is not None:
            conditions['ciMa'] = ciMa
        return crudReturn([asdict(ast) for ast in AssistsAp.filter(conditions)])
    else:
        data = request.get_json()
        if request.method == 'POST':
            return crudReturn(asdict(AssistsAp(**data).save()))
        if request.method == 'PUT' or request.method == 'PATCH':
            return crudReturn([asdict(asa) for asa in AssistsAp.update(data)])
        if request.method == 'DELETE':
            return crudReturn(AssistsAp.delete(data))
        
@router.route('/attendsTo', methods=['POST', 'PUT', 'PATCH', 'GET', 'DELETE']) # POST | PUT | PATCH | GET | DELETE /api/appointment/attendsTo
@router.get('/attendsTo/<int:idAp>')
@router.get('/attendsTo/ciPa/<int:ciPa>')
def attendsTo(idAp:int=None,ciPa:int=None): # a [patient] <attends to> an [appointment] 
    if request.method == 'GET':
        conditions = {}
        if idAp is not None:
            conditions['idAp'] = idAp
        if ciPa is not None:
            conditions['ciPa'] = ciPa
        return crudReturn([asdict(ast) for ast in AttendsTo.filter(conditions)])
    else:
        data = request.get_json()
        if request.method == 'POST':
            return crudReturn(asdict(AttendsTo(**data).save()))
        if request.method == 'PUT' or request.method == 'PATCH':
            return crudReturn([asdict(att) for att in AttendsTo.update(data)])
        if request.method == 'DELETE':
            return crudReturn(AttendsTo.delete(data))
        
# # -- DATA INPUTTED WHEN A PATIENT IS BEING INTERVIEWED IN AN APPOINTMENT

@router.route('/diagnoses', methods=['POST', 'DELETE']) # POST | DELETE /api/appointment/diagnoses
@router.get('/diagnoses/<int:idAp>/<int:ciPa>') # GET /api/appointment/diagnoses/<idAp>
def diagnosedDisease(idAp:int=None, ciPa:int=None): # input diagnosed diseases
    if request.method == 'GET':
        result = [asdict(d) for d in Diagnoses.filter({'idAp': idAp, 'ciPa': ciPa})]
        for d in result:
            d['name'] = Disease.getById(d['idDis']).name
    else:
        data = request.get_json()['diagnoses']
        result = []

        for d in data:
            if request.method == 'POST':
                if d.get('idDis', None) is None:
                    _d = Disease(name=d['name']).saveOrGet(['name'])
                    d['idDis'] = _d.id
                    d.pop('name')

                diagnosesInstance = Diagnoses(**d).save()
                diagnosesReturn = asdict(diagnosesInstance)
                diagnosesReturn['name'] = Disease.getById(d['idDis']).name
                result.append(diagnosesReturn)

            elif request.method == 'DELETE':
                Diagnoses.delete(d)
                result = True

    return crudReturn(result)

@router.route('/registersSy', methods=['POST', 'DELETE']) # POST | DELETE /api/appointment/registersSy
@router.get('/registersSy/<int:idAp>/<int:ciPa>') # GET /api/appointment/registersSy/<idAp>
def registersSy(idAp:int=None,ciPa:int=None): # input registered symptoms
    if request.method == 'GET':
        result = [asdict(sy) for sy in RegistersSy.filter({'idAp': idAp,'ciPa': ciPa})]
        for sy in result:
            sy['name'] = Symptom.getById(sy['idSy']).name
    else:
        data = request.get_json()['registersSy']
        result = []

        for s in data:
            if request.method == 'POST':
                if s.get('idSy', None) is None:
                    _s = Symptom(name=s['name']).saveOrGet(['name'])
                    s['idSy'] = _s.id
                    s.pop('name')

                registersSyInstance = RegistersSy(**s).save()
                registersSyReturn = asdict(registersSyInstance)
                registersSyReturn['name'] = Symptom.getById(s['idSy']).name
                result.append(registersSyReturn)

            elif request.method == 'DELETE':
                RegistersSy.delete(s)
                result = True

    return crudReturn(result)

@router.route('/registersCs', methods=['POST', 'DELETE']) # POST | DELETE /api/appointment/registersCs
@router.get('/registersCs/<int:idAp>/<int:ciPa>') # GET /api/appointment/registersCs/<idAp>
def registersCs(idAp:int=None, ciPa:int=None): # input registered clinical signs
    if request.method == 'GET':
        result = [asdict(cs) for cs in RegistersCs.filter({'idAp': idAp, 'ciPa': ciPa})]
        for cs in result:
            cs['name'] = ClinicalSign.getById(cs['idCs']).name
    else:
        data = request.get_json()['registersCs']
        result = []

        for cs in data:
            if request.method == 'POST':
                if cs.get('idCs', None) is None:
                    _cs = ClinicalSign(name=cs['name']).saveOrGet(['name'])
                    cs['idCs'] = _cs.id
                    cs.pop('name')
                
                registersCsInstance = RegistersCs(**cs).save()
                registersCsReturn = asdict(registersCsInstance)
                registersCsReturn['name'] = ClinicalSign.getById(cs['idCs']).name
                result.append(registersCsReturn)

            elif request.method == 'DELETE':
                RegistersCs.delete(cs)
                result = True

    return crudReturn(result)