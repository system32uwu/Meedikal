from models.ClinicalSign import ClinicalSign, RegistersCs
from models.Disease import Disease, Diagnoses
from models.Symptom import Symptom, RegistersSy
from flask import Blueprint, request

from util.crud import *
from util.returnMessages import *

from models.Appointment import *

router = Blueprint('appointment', __name__, url_prefix='/appointment')

@router.route('', methods=['GET', 'DELETE']) # GET | DELETE /api/appointment
def apById():
    return crudv2(Appointment,request)

@router.route('', methods=['POST', 'PUT', 'PATCH']) # POST | PUT | PATCH /api/appointment
def createOrUpdate():
    return crudv2(Appointment,request, createWithoutFiltering=True if request.method == 'POST' else False)

@router.route('/assignedTo', methods=['POST','PATCH', 'PUT', 'DELETE', 'GET'])
def assignedTo():
    return crudv2(request,AssignedTo)

@router.route('/assistsAp', methods=['POST','PATCH', 'PUT', 'DELETE', 'GET'])
def assistsAp():
    return crudv2(request,AssistsAp)

@router.route('/attendsTo', methods=['POST', 'PATCH', 'PUT', 'DELETE', 'GET'])
def patientAttendsToAp():
    return crudv2(AttendsTo,request)

# -- DATA INPUTTED WHEN A PATIENT IS BEING INTERVIEWED IN AN APPOINTMENT

@router.route('/patientApData/apRefPrevAp', methods=['POST','PUT','PATCH','DELETE', 'GET'])
def apRefPrevAp(): # input a reference to a previous appointment
    return crudv2(ApRefPrevAp,request)

@router.route('/patientApData/apRefExam', methods=['POST', 'PUT', 'PATCH','DELETE', 'GET'])
def apRefExam(): # input a reference to an exam
    return crudv2(ApRefExam,request)

@router.route('/patientApData/apRefTr', methods=['POST','PUT', 'PATCH','DELETE', 'GET'])
def apRefTr(): # input a reference to a treatment
    return crudv2(ApRefTr,request)

@router.route('/patientApData/fills', methods=['POST','PUT', 'PATCH','DELETE', 'GET'])
def fills(): # input a response to a question of the interview
    return crudv2(Fills,request)

@router.route('/patientApData/suggestsTr', methods=['POST','PUT', 'PATCH','DELETE', 'GET'])
def suggestsTrs(): # input suggested treatments
    return crudv2(SuggestsTr,request)

@router.route('/patientApData/requiresEx', methods=['POST','PUT', 'PATCH','DELETE', 'GET'])
def requiredExams(): # input required exams 
    return crudv2(RequiresEx,request)

@router.route('/patientApData/diagnoses', methods=['POST', 'GET'])
def diagnosedDisease(): # input diagnosed disease
    if request.method == 'POST':
        data = json.loads(request.data)

        diagnoses = data['diagnoses']

        diseases = [getOrCreate(Disease, Disease(name=disease['name']), f"name = '{disease['name']}'") 
                                for disease in diagnoses]
            
        for disease in diseases:
            for _d in diagnoses:
                if _d['name'] == disease[0][0].name:
                    _d['idDis'] = disease[0][0].id
                _d.pop('name', None)

        request.data = json.dumps({Diagnoses.__tablename__: diagnoses})

    return crudv2(Diagnoses,request)

@router.route('/patientApData/registersSy', methods=['POST', 'GET'])
def registersSy(): # input registered symptoms
    if request.method == 'POST':
        data = json.loads(request.data)

        registersSy = data['registersSy']

        symptoms = [getOrCreate(Symptom, Symptom(name=symptom['name']), f"name = '{symptom['name']}'") 
                                for symptom in registersSy]
            
        for symptom in symptoms:
            for _d in registersSy:
                if _d['name'] == symptom[0][0].name:
                    _d['idSy'] = symptom[0][0].id
                _d.pop('name', None)

        request.data = json.dumps({RegistersSy.__tablename__: registersSy})

    return crudv2(RegistersSy,request)

@router.route('/patientApData/registersCs', methods=['POST', 'GET'])
def registersSc(): # input registered clinical signs
    if request.method == 'POST':
        data = json.loads(request.data)

        registersCs = data['registersCs']

        clinicalSigns = [getOrCreate(ClinicalSign, ClinicalSign(name=clinicalSign['name']), f"name = '{clinicalSign['name']}'") 
                                for clinicalSign in registersCs]
            
        for clinicalSign in clinicalSigns:
            for _d in registersCs:
                if _d['name'] == clinicalSign[0][0].name:
                    _d['idCs'] = clinicalSign[0][0].id
                _d.pop('name', None)

        request.data = json.dumps({RegistersCs.__tablename__: registersCs})

    return crudv2(RegistersCs,request)