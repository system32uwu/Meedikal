from dataclasses import asdict
from flask import json, jsonify, Blueprint, request

from sqlalchemy import and_, or_
from sqlalchemy.sql.expression import table

from util.crud import *
from util.returnMessages import *

from models.Appointment import *

router = Blueprint('appointment', __name__, url_prefix='/appointment')

@router.route('/<int:id>', methods=['GET','DELETE']) # GET | DELETE /api/appointment/{id}
def apById(id):
    ap = asdict(Appointment.query.filter(Appointment.id==id).one_or_none())
    return crud(request.method, model=Appointment,obj=ap,
                messageReturn=True if request.method == 'DELETE' else False,
                jsonReturn=True if request.method == 'GET' else False,id=id)

@router.route('', methods=['POST', 'PUT', 'PATCH']) # POST | PUT | PATCH /api/appointment
def createOrUpdate():

    try:
        apData = json.loads(request.data)

        ap = Appointment(name=apData['name'], date=apData.get('date', None),
                         state=apData.get('state','OK'), timeBegins=apData.get('timeBegins', None), 
                         timeEnds=apData.get('timeEnds', None), etpp=apData.get('etpp', None),
                         maxTurns=apData.get('maxTurns', None))

        return crud(request.method,Appointment,ap,messageReturn=True,id=ap.id)
    except:
        return provideData()

@router.route('/medicalAssistantAssistsAp', methods=['POST','PATCH', 'PUT', 'DELETE'])
def medicalAssistantAssistsAp():
    
    try:
        assistsData = json.loads(request.data)
        aP = AssistsAp(idAp=assistsData['idAp'], ciMa=assistsData['ciMa'],
                       time=assistsData['time'])
        
        return crud(request.method,AssistsAp,aP)
    except:
        return provideData()

@router.route('/pattientAttendsToAp', methods=['POST', 'PATCH', 'PUT', 'DELETE'])
def patientAttendsToAp():

    try:
        attendsToData = json.loads(request.data)
        aT = AttendsTo(idAp=attendsToData['idAp'], ciPa=attendsToData['ciPa'],
                       motive=attendsToData.get('motive', None), number=attendsToData.get('number', None),
                       time=attendsToData.get('time', None))
        
        return crud(request.method,AttendsTo,aT, idAp=aT.idAp, ciPa=aT.ciPa)

    except:
        return provideData()

# @router.route('/patientApData', methods=['POST','PUT','PATCH','DELETE']) # TODO: handle when some data is not provided, everything here is actually optional data.
# def patientApData():
#     try:
#         data = json.loads(request.data)
        
#         apRefPrevApData = data.get('apRefPrevAp') # references to previous appointments

#         apRefExamData = data.get('apRefExam') # references to exams that the patient did
#         apRefTrData = data.get('apRefTr') # references to treatments that the patient did / is doing
        
#         fillsData = data.get('fills') # responses to form's questions
        
#         suggestsTrData = data.get('suggestsTr') # suggested treatments
#         requiresExData = data.get('requiresEx') # requiredExams
        
#         diagnosesData = data.get('diagnoses') # diagnosed illness
#         registersSyData = data.get('registersSy') # registered symptoms
#         registersScData = data.get('registersSc') # registered clinical signs

#         if apRefPrevApData is not None:
#             apRefs = [ApRefPrevAp(idCurrAp=ref['idCurrAp'],
#                                   ciPaCurrAp=ref['ciPa'],
#                                   idPrevAp=ref['idPrevAp'],
#                                   ciPaPrevAp=ref['ciPa']) for ref in apRefPrevApData]

#             for apRef in apRefs:
#                 if request.method == 'POST':
#                     apRefPrevAp, created = (getOrCreate(ApRefPrevAp,toInsert=apRef,
#                                         idCurrAp=apRef.idCurrAp,ciPaCurrAp=apRef.ciPaCurrAp,
#                                         idPrevAp=apRef.idPrevAp,ciPaPrevAp=apRef.ciPaPrevAp))
#                     if not created:
#                         return recordAlreadyExists('apRefPrevAp')
#                 elif request.method == 'PUT':
#                     apRefPrevAp, putted = (put(ApRefPrevAp,toPut=apRef,
#                                         idCurrAp=apRef.idCurrAp,ciPaCurrAp=apRef.ciPaCurrAp,
#                                         idPrevAp=apRef.idPrevAp,ciPaPrevAp=apRef.ciPaPrevAp))
#                     if not putted:
#                         return recordDoesntExist('apRefPrevAp')
#                 elif request.method == 'PATCH':
#                     apRefPrevAp, patched = (patch(ApRefPrevAp,toPatch=apRef,
#                                         idCurrAp=apRef.idCurrAp,ciPaCurrAp=apRef.ciPaCurrAp,
#                                         idPrevAp=apRef.idPrevAp,ciPaPrevAp=apRef.ciPaPrevAp))
#                     if not patched:
#                         return recordDoesntExist('apRefPrevAp')
#                 elif request.method == 'DELETE':
#                     deleted = delete(ApRefPrevAp,
#                                     idCurrAp=apRef.idCurrAp,ciPaCurrAp=apRef.ciPaCurrAp,
#                                     idPrevAp=apRef.idPrevAp,ciPaPrevAp=apRef.ciPaPrevAp)
#                     if not deleted:
#                         return recordDoesntExist('apRefPrevAp')
        
#         if apRefExamData is not None:

#             apRefExams = [ApRefExam(idAp=ref['idAp'],
#                                 ciPaAp=ref['ciPa'],
#                                 idExTaken=ref['idExTaken'],
#                                 idEx=ref['idEx'],
#                                 ciPaEx=ref['ciPa']) for ref in apRefExamData]
#             for apRef in apRefExams:
#                 if request.method == 'POST':
#                     apRefExam, created = (getOrCreate(ApRefExam,toInsert=apRef,
#                                         idAp=apRef.idAp,ciPaAp=apRef.ciPaAp,
#                                         idExTaken=apRef.idExTaken,idEx=apRef.idEx,
#                                         ciPaEx=apRef.ciPaEx))
#                     if not created:
#                         return recordAlreadyExists('apRefExam')
#                 elif request.method == 'PUT':
#                     apRefExam, putted = (put(ApRefExam,toPut=apRef,
#                                         idAp=apRef.idAp,ciPaAp=apRef.ciPaAp,
#                                         idExTaken=apRef.idExTaken,idEx=apRef.idEx,
#                                         ciPaEx=apRef.ciPaEx))
#                     if not putted:
#                         return recordDoesntExist('apRefExam')
#                 elif request.method == 'PATCH':
#                     apRefExam, patched = (patch(ApRefExam,toPatch=apRef,
#                                         idAp=apRef.idAp,ciPaAp=apRef.ciPaAp,
#                                         idExTaken=apRef.idExTaken,idEx=apRef.idEx,
#                                         ciPaEx=apRef.ciPaEx))
#                     if not patched:
#                         return recordDoesntExist('apRefExam')
#                 elif request.method == 'DELETE':
#                     deleted = delete(ApRefExam,
#                                      idAp=apRef.idAp,ciPaAp=apRef.ciPaAp,
#                                      idExTaken=apRef.idExTaken,idEx=apRef.idEx,
#                                      ciPaEx=apRef.ciPaEx)
#                     if not deleted:
#                         return recordDoesntExist('apRefExam')
        
#         apRefTr = ApRefTr(idAp=apRefTrData['idAp'],
#                           ciPaAp=apRefTrData['ciPaAp'],
#                           idFollows=apRefTrData['idFollows'],
#                           idTreatment=apRefTrData['idTreatment'],
#                           ciPaTr=apRefTrData['ciPaAp'])

#         suggestsTr = SuggestsTr(idAp=suggestsTrData['idAp'],
#                                 ciPaAp=suggestsTrData['ciPaAp'],
#                                 idTreatment=suggestsTrData['idTreatment'])

#         requiresEx = RequiresEx(idAp=requiresExData['idAp'],
#                                 ciPaAp=requiresExData['ciPaAp'],
#                                 idEx=requiresExData['idExam'])

#         fills = [Fills(idAp=fill['idAp'],ciPa=fill['ciPa'],
#                        idForm=fill['idForm'], idQuestion=fill['idQuestion'],
#                        response=fill['response']) for fill in fillsData]
#         return recordCUDSuccessfully(tablename='patientApData',create=True)

#     except Exception: # any other exception ocurred
#         return provideData()