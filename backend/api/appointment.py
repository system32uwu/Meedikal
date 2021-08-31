from dataclasses import asdict
from operator import and_
from flask import json, Blueprint, request

from util.crud import *
from util.returnMessages import *

from models.Appointment import *

router = Blueprint('appointment', __name__, url_prefix='/appointment')

@router.get('') # GET /api/appointment
def apById():
    ap = asdict(Appointment.query.filter(Appointment.id==json.loads(request.data)['id']).one_or_none())
    return crudv2(request=request,preparedResult=ap)

@router.delete('') # DELETE /api/appointment
def apById():
    return crudv2(Appointment,request)

@router.route('', methods=['POST', 'PUT', 'PATCH']) # POST | PUT | PATCH /api/appointment
def createOrUpdate():
    return crudv2(Appointment,request, createWithoutFiltering=True)

@router.route('/assistsAp', methods=['POST','PATCH', 'PUT', 'DELETE'])
def assistsAp():
    return crudv2(request,AssistsAp)

@router.route('/pattientAttendsToAp', methods=['POST', 'PATCH', 'PUT', 'DELETE'])
def patientAttendsToAp():

    try:
        attendsToData = json.loads(request.data)
        aT = AttendsTo(idAp=attendsToData['idAp'], ciPa=attendsToData['ciPa'],
                       motive=attendsToData.get('motive', None), number=attendsToData.get('number', None),
                       time=attendsToData.get('time', None))
        
        return crudv2(request.method,AttendsTo,aT, idAp=aT.idAp, ciPa=aT.ciPa)
    except:
        return provideData()

# -- DATA INPUTTED WHEN A PATIENT IS BEING INTERVIEWED IN AN APPOINTMENT

@router.route('/patientApData/apRefPrevAp', methods=['POST','PUT', 'PATCH','DELETE'])
def apRefPrevAp(): # input a reference to a previous appointment
        try:
            data = json.loads(request.data)

            apRefPrevApData = data['apRefPrevAp'] # references to previous appointments

            apRefs = [ApRefPrevAp(idCurrAp=ref['idCurrAp'],
                                  ciPaCurrAp=ref['ciPa'],
                                  idPrevAp=ref['idPrevAp'],
                                  ciPaPrevAp=ref['ciPa']) for ref in apRefPrevApData]

            if request.method == 'DELETE':
                return crudv2(request.method, ApRefPrevAp, idCurrAp=apRefs[0].idCurrAp,ciPaCurrAp=apRefs[0].ciPaCurrAp)

            elif request.method == 'PUT' or request.method == 'PATCH':
                delete(ApRefPrevAp, idCurrAp=apRefs[0].idCurrAp,ciPaCurrAp=apRefs[0].ciPaCurrAp)
            
            for apRef in apRefs:
                result, opState = (crudv2('POST',ApRefPrevAp,apRef, tupleReturn=True,
                              idCurrAp=apRef.idCurrAp,ciPaCurrAp=apRef.ciPaCurrAp,
                              idPrevAp=apRef.idPrevAp,ciPaPrevAp=apRef.ciPaPrevAp))
                if not opState:
                    if request.method == 'POST':
                        return recordAlreadyExists(ApRefPrevAp.__tablename__, asdict(apRef))
            
            return recordCUDSuccessfully(ApRefPrevAp.__tablename__, request.method)

        except:
            return provideData()

@router.get('/patientApData/apRefPrevAp/<int:idAp>/<int:ciPa>') # GET references to appointments of an appointment
def getApRefPrevAp(idAp:int,ciPa:int): 
        appointments = [asdict(ap) for ap in ApRefPrevAp.query.filter(and_(
                        ApRefPrevAp.idCurrAp == idAp,
                        ApRefPrevAp.ciPaCurrAp == ciPa)).all()]
        return crudv2(request.method,ApRefPrevAp,appointments)

@router.route('/patientApData/apRefExam', methods=['POST','PUT', 'PATCH','DELETE'])
def apRefExam(): # input a reference to an exam
        try:
            data = json.loads(request.data)

            apRefExamData = data['apRefExam']

            apRefs = [ApRefExam(idAp=ref['idAp'],
                                ciPaAp=ref['ciPaAp'],
                                idExTaken=ref['idExTaken'],
                                idEx=ref['idEx'],
                                ciPaEx=ref['ciPaEx'])
                                for ref in apRefExamData]

            if request.method == 'DELETE':
                return crudv2(request.method, ApRefExam, idAp=apRefs[0].idAp,ciPaAp=apRefs[0].ciPaAp)

            elif request.method == 'PUT' or request.method == 'PATCH':
                delete(ApRefExam, idAp=apRefs[0].idAp,ciPaAp=apRefs[0].ciPaAp)
            
            for apRef in apRefs:
                result, opState = (crudv2('POST',ApRefExam,apRef, tupleReturn=True,
                                  idAp=apRef.idAp,ciPaAp=apRef.ciPaAp, idExTaken=apRef.idExTaken,
                                  idEx=apRef.idEx,ciPaEx=apRef.ciPaEx))
                if not opState:
                    if request.method == 'POST':
                        return recordAlreadyExists(ApRefExam.__tablename__, asdict(apRef))
            
            return recordCUDSuccessfully(ApRefExam.__tablename__, request.method)

        except:
            return provideData()

@router.get('/patientApData/apRefExam/<int:idAp>/<int:ciPa>') # GET references to exams of an appointment
def getApRefExam(idAp:int,ciPa:int):
        apRefs = [asdict(apRef) for apRef in ApRefExam.query.filter(and_(
                        ApRefExam.idAp == idAp,
                        ApRefExam.ciPaAp == ciPa)).all()]
        return crudv2(request.method,ApRefExam,apRefs)

@router.route('/patientApData/apRefTr', methods=['POST','PUT', 'PATCH','DELETE'])
def apRefTr(): # input a reference to a treatment
        try:
            data = json.loads(request.data)

            apRefTrData = data['apRefTr']

            apRefs = [ApRefTr(idAp=ref['idAp'],
                              ciPaAp=ref['ciPaAp'],
                              idFollows=ref['idFollows'],
                              idTreatment=ref['idTreatment'],
                              ciPaTr=ref['ciPaTr'])
                              for ref in apRefTrData]

            if request.method == 'DELETE':
                return crudv2(request.method, ApRefTr, idAp=apRefs[0].idAp,ciPaAp=apRefs[0].ciPaAp)

            elif request.method == 'PUT' or request.method == 'PATCH':
                delete(ApRefTr, idAp=apRefs[0].idAp,ciPaAp=apRefs[0].ciPaAp)
            
            for apRef in apRefs:
                result, opState = (crudv2('POST',ApRefTr,apRef, tupleReturn=True,
                                  idAp=apRef.idAp,ciPaAp=apRef.ciPaAp, idFollows=apRef.idFollows,
                                  idTreatment=apRef.idTreatment,ciPaTr=apRef.ciPaTr))
                if not opState:
                    if request.method == 'POST':
                        return recordAlreadyExists(ApRefTr.__tablename__, asdict(apRef))
            
            return recordCUDSuccessfully(ApRefTr.__tablename__, request.method)

        except:
            return provideData()

@router.get('/patientApData/apRefTr/<int:idAp>/<int:ciPa>') # GET references to treatments of an appointment
def getApRefTr(idAp:int,ciPa:int):
        apRefs = [asdict(apRef) for apRef in ApRefTr.query.filter(and_(
                        ApRefTr.idAp == idAp,
                        ApRefTr.ciPaAp == ciPa)).all()]
        return crudv2(request.method,ApRefTr,apRefs)

@router.route('/patientApData/fills', methods=['POST','PUT', 'PATCH','DELETE'])
def fills(): # input a response to a question of the interview
        try:
            data = json.loads(request.data)

            fillsData = data['fills']

            _fills = [Fills(idAp=ref['idAp'],
                            ciPa=ref['ciPa'],
                            idForm=ref['idForm'],
                            idQuestion=ref['idQuestion'],
                            response=ref.get('response', None))
                            for ref in fillsData]

            if request.method == 'DELETE':
                return crudv2(request.method, Fills, idAp=_fills[0].idAp,ciPa=_fills[0].ciPa)

            elif request.method == 'PUT' or request.method == 'PATCH':
                delete(Fills, idAp=_fills[0].idAp,ciPa=_fills[0].ciPa)
            
            for fill in _fills:
                result, opState = (crudv2('POST',Fills,_fills, tupleReturn=True,
                                  idAp=fill.idAp,ciPa=fill.ciPa, idForm=fill.idForm,
                                  idQuestion=fill.idQuestion))
                if not opState:
                    if request.method == 'POST':
                        return recordAlreadyExists(Fills.__tablename__, asdict(fill))
            
            return recordCUDSuccessfully(Fills.__tablename__, request.method)
        except:
            return provideData()

@router.get('/patientApData/fills/<int:idAp>/<int:ciPa>') # GET the questions answered during an appointment
def getFills(idAp:int,ciPa:int):
        fills = [asdict(fill) for fill in Fills.query.filter(and_(
                        Fills.idAp == idAp,
                        Fills.ciPa == ciPa)).all()]
        return crudv2(request.method,Fills,fills)

@router.route('/patientApData/suggestsTr', methods=['POST','PUT', 'PATCH','DELETE'])
def suggestsTrs(): # input suggested treatments when concluding the appointment
        try:
            data = json.loads(request.data)

            apSuggestedTrData = data['suggestsTr']

            apRefs = [SuggestsTr(idAp=ref['idAp'],
                                 ciPaAp=ref['ciPaAp'],
                                 idTreatment=ref['idTreatment'])
                                 for ref in apSuggestedTrData]

            if request.method == 'DELETE':
                return crudv2(request.method, SuggestsTr, idAp=apRefs[0].idAp,ciPaAp=apRefs[0].ciPaAp)

            elif request.method == 'PUT' or request.method == 'PATCH':
                delete(SuggestsTr, idAp=apRefs[0].idAp,ciPaAp=apRefs[0].ciPaAp)
            
            for apRef in apRefs:
                result, opState = (crudv2('POST',SuggestsTr,apRef, tupleReturn=True,
                                  idAp=apRef.idAp,ciPaAp=apRef.ciPaAp, 
                                  idTreatment=apRef.idTreatment))
                if not opState:
                    if request.method == 'POST':
                        return recordAlreadyExists(SuggestsTr.__tablename__, asdict(apRef))
            
            return recordCUDSuccessfully(SuggestsTr.__tablename__, request.method)

        except:
            return provideData()

@router.get('/patientApData/suggestsTr/<int:idAp>/<int:ciPa>') # GET references to suggested treatments of an appointment
def getSuggestedTrs(idAp:int,ciPa:int):
        suggestedTrs = [asdict(sgtr) for sgtr in SuggestsTr.query.filter(and_(
                        SuggestsTr.idAp == idAp,
                        SuggestsTr.ciPaAp == ciPa)).all()]
        return crudv2(request.method,SuggestsTr,suggestedTrs)

@router.route('/patientApData/suggestsTr', methods=['POST','PUT', 'PATCH','DELETE'])
def requiredExams(): # input required exams when concluding the appointment
        try:
            data = json.loads(request.data)

            apRequiresExData = data['requiresEx']

            apRefs = [RequiresEx(idAp=ref['idAp'],
                                 ciPaAp=ref['ciPaAp'],
                                 idEx=ref['idEx'])
                                 for ref in apRequiresExData]

            if request.method == 'DELETE':
                return crudv2(request.method, RequiresEx, idAp=apRefs[0].idAp,ciPaAp=apRefs[0].ciPaAp)

            elif request.method == 'PUT' or request.method == 'PATCH':
                delete(RequiresEx, idAp=apRefs[0].idAp,ciPaAp=apRefs[0].ciPaAp)
            
            for apRef in apRefs:
                result, opState = (crudv2('POST',RequiresEx,apRef, tupleReturn=True,
                                  idAp=apRef.idAp,ciPaAp=apRef.ciPaAp, 
                                  idEx=apRef.idEx))
                if not opState:
                    if request.method == 'POST':
                        return recordAlreadyExists(RequiresEx.__tablename__, asdict(apRef))
            
            return recordCUDSuccessfully(RequiresEx.__tablename__, request.method)

        except:
            return provideData()

@router.get('/patientApData/requiresEx/<int:idAp>/<int:ciPa>') # GET references to required exams of an appointment
def getRequiredExams(idAp:int,ciPa:int):
        requiredExs = [asdict(rqEx) for rqEx in RequiresEx.query.filter(and_(
                        RequiresEx.idAp == idAp,
                        RequiresEx.ciPaAp == ciPa)).all()]
        return crudv2(request.method,RequiresEx,requiredExs)

# @router.route('/patientApData', methods=['POST','PUT','PATCH','DELETE'])
# def patientApData():
#     try:
#         data = json.loads(request.data)
        
#         diagnosesData = data.get('diagnoses') # diagnosed illness
#         registersSyData = data.get('registersSy') # registered symptoms
#         registersScData = data.get('registersSc') # registered clinical signs
        
#         return recordCUDSuccessfully(tablename='patientApData',create=True)

#     except Exception: # any other exception ocurred
#         return provideData()