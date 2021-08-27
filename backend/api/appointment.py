from dataclasses import asdict
from flask import json, jsonify, Blueprint, request

from sqlalchemy import and_, or_
from sqlalchemy.sql.expression import table

from util.crud import *
from util.returnMessages import *

from models.Appointment import *

router = Blueprint('appointment', __name__, url_prefix='/appointment')

@router.route('/<int:id>', methods=['GET','DELETE']) # GET | DELETE /api/appointment/{id}
def hello(id):
    appointment = Appointment.query.filter(Appointment.id==id).first()

    if appointment is None:
        return recordDoesntExists('appointment')
    else:
        if request.method == 'GET':
            return jsonify(asdict(appointment)), 200
        else:
            appointment.delete()
            return recordCUDSuccessfully(delete=True)

@router.route('', methods=['POST', 'PUT', 'PATCH']) # POST | PUT | PATCH /api/appointment
def createOrUpdate():

    try:
        apData = json.loads(request.data)

        ap = Appointment(name=apData['name'], date=apData['date'],
                         state=apData['state'], timeBegins=apData.get('timeBegins', None), 
                         timeEnds=apData.get('timeEnds', None), etpp=apData.get('etpp', None),
                         maxTurns=apData.get('maxTurns', None))
        
        ciDoc = apData['ciDoc']

        if request.method == 'POST':
            appointment, created = (getOrCreate(model=Appointment, toInsert=ap, id=ap.id))

            if not created:
                return recordAlreadyExists()
            else:
                asigned = AssignedTo(idAp=appointment.id, ciDoc=ciDoc)
                getOrCreate(model=AssignedTo,toInsert=asigned, idAp=ap.id, ciDoc=ciDoc)

                return recordCUDSuccessfully('appointment',create=True)
        if request.method == 'PUT':
            ap.id = apData['id']
            appointment, putted = (put(Appointment,ap,id=ap.id))
            if not putted:
                return recordDoesntExists('appointment')
            else:
                asigned = AssignedTo(idAp=appointment.id, ciDoc=ciDoc)
                _asigned, _putted = (put(model=AssignedTo,toInsert=asigned, idAp=ap.id))
                if not _putted:
                    return recordDoesntExists("assignedTo")
                else:
                    return recordCUDSuccessfully('appointment',update=True)
        elif request.method == 'PATCH':
            ap.id = apData['id']
            appointment, patched = (patch(Appointment,ap,id=ap.id))
            if not patched:
                return recordDoesntExists('appointment')
            else:
                return recordCUDSuccessfully('appointment',update=True)
    except:
        return provideData()

@router.route('/medicalAssistantAssistsAp', methods=['POST','PATCH', 'PUT', 'DELETE'])
def medicalAssistantAssistsAp():
    
    try:
        assistsData = json.loads(request.data)
        aP = AssistsAp(idAp=assistsData['idAp'], ciMa=assistsData['ciMa'],
                       time=assistsData['time'])
        
        if request.method == 'POST':
            assistsAp, created = (getOrCreate(AssistsAp,toInsert=aP,idAp=aP.idAp,ciMa=aP.ciMa, time=aP.time))

            if not created:
                return recordAlreadyExists('assistsAp')
            else:
                return recordCUDSuccessfully('assistsAp', create=True)
        elif request.method == 'PATCH':
            assistsAp, patched = (patch(AssistsAp,toPatch=aP,idAp=aP.idAp,ciMa=aP.ciMa, time=aP.time))

            if not patched:
                return recordDoesntExists('assistsAp')
            else:
                return recordCUDSuccessfully('assistsAp', update=True)
        elif request.method == 'PUT':
            assistsAp, putted = (put(AssistsAp,toPut=aP,idAp=aP.idAp,ciMa=aP.ciMa, time=aP.time))

            if not putted:
                return recordDoesntExists('assistsAp')
            else:
                return recordCUDSuccessfully('assistsAp', update=True)
        elif request.method == 'DELETE':
            deleted = delete(AssistsAp,idAp=aP.idAp,ciMa=aP.ciMa, time=aP.time)

            if not deleted:
                return recordDoesntExists('assistsAp')
            else:
                return recordCUDSuccessfully('assistsAp', delete=True)
    except:
        return provideData()

@router.route('/pattientAttendsToAp', methods=['POST', 'PATCH', 'PUT', 'DELETE'])
def patientAttendsToAp():

    try:
        attendsToData = json.loads(request.data)
        aT = AttendsTo(idAp=attendsToData['idAp'], ciPa=attendsToData['ciPa'],
                       motive=attendsToData.get('motive', None), number=attendsToData.get('number', None),
                       time=attendsToData.get('time', None))
        
        if request.method == 'POST':
            attendsTo, created = (getOrCreate(AttendsTo,toInsert=aT,idAp=aT.idAp,ciPa=aT.ciPa))

            if not created:
                return recordAlreadyExists('attendsTo')
            else:
                return recordCUDSuccessfully('attendsTo', create=True)
        elif request.method == 'PATCH':
            attendsTo, patched = (patch(AttendsTo,toPatch=aT,idAp=aT.idAp,ciPa=aT.ciPa))

            if not patched:
                return recordDoesntExists('attendsTo')
            else:
                return recordCUDSuccessfully('attendsTo', update=True)
        elif request.method == 'PUT':
            attendsTo, putted = (put(AttendsTo,toPut=aT,idAp=aT.idAp,ciPa=aT.ciPa))

            if not putted:
                return recordDoesntExists('attendsTo')
            else:
                return recordCUDSuccessfully('attendsTo', update=True)
        elif request.method == 'DELETE':
            deleted = delete(AttendsTo,idAp=aT.idAp,ciPa=aT.ciPa)

            if not deleted:
                return recordDoesntExists('attendsTo')
            else:
                return recordCUDSuccessfully('attendsTo', delete=True)
    except:
        return provideData()

@router.route('/patientApData', methods=['POST','PUT','PATCH','DELETE']) # TODO: handle when some data is not provided, everything here is actually optional data.
def patientApData():
    try:
        data = json.loads(request.data)
        
        apRefPrevApData = data.get('apRefPrevAp') # references to previous appointments

        apRefExamData = data.get('apRefExam') # references to exams that the patient did
        apRefTrData = data.get('apRefTr') # references to treatments that the patient did / is doing
        
        fillsData = data.get('fills') # responses to form's questions
        
        suggestsTrData = data.get('suggestsTr') # suggested treatments
        requiresExData = data.get('requiresEx') # requiredExams
        
        diagnosesData = data.get('diagnoses') # diagnosed illness
        registersSyData = data.get('registersSy') # registered symptoms
        registersScData = data.get('registersSc') # registered clinical signs

        if apRefPrevApData is not None:
            apRefs = [ApRefPrevAp(idCurrAp=ref['idCurrAp'],
                                  ciPaCurrAp=ref['ciPa'],
                                  idPrevAp=ref['idPrevAp'],
                                  ciPaPrevAp=ref['ciPa']) for ref in apRefPrevApData]

            for apRef in apRefs:
                if request.method == 'POST':
                    apRefPrevAp, created = (getOrCreate(ApRefPrevAp,toInsert=apRef,
                                        idCurrAp=apRef.idCurrAp,ciPaCurrAp=apRef.ciPaCurrAp,
                                        idPrevAp=apRef.idPrevAp,ciPaPrevAp=apRef.ciPaPrevAp))
                    if not created:
                        return recordAlreadyExists('apRefPrevAp')
                elif request.method == 'PUT':
                    apRefPrevAp, putted = (put(ApRefPrevAp,toPut=apRef,
                                        idCurrAp=apRef.idCurrAp,ciPaCurrAp=apRef.ciPaCurrAp,
                                        idPrevAp=apRef.idPrevAp,ciPaPrevAp=apRef.ciPaPrevAp))
                    if not putted:
                        return recordDoesntExists('apRefPrevAp')
                elif request.method == 'PATCH':
                    apRefPrevAp, patched = (patch(ApRefPrevAp,toPatch=apRef,
                                        idCurrAp=apRef.idCurrAp,ciPaCurrAp=apRef.ciPaCurrAp,
                                        idPrevAp=apRef.idPrevAp,ciPaPrevAp=apRef.ciPaPrevAp))
                    if not patched:
                        return recordDoesntExists('apRefPrevAp')
                elif request.method == 'DELETE':
                    deleted = delete(ApRefPrevAp,
                                    idCurrAp=apRef.idCurrAp,ciPaCurrAp=apRef.ciPaCurrAp,
                                    idPrevAp=apRef.idPrevAp,ciPaPrevAp=apRef.ciPaPrevAp)
                    if not deleted:
                        return recordDoesntExists('apRefPrevAp')
        
        if apRefExamData is not None:

            apRefExams = [ApRefExam(idAp=ref['idAp'],
                                ciPaAp=ref['ciPa'],
                                idExTaken=ref['idExTaken'],
                                idEx=ref['idEx'],
                                ciPaEx=ref['ciPa']) for ref in apRefExamData]
            for apRef in apRefExams:
                if request.method == 'POST':
                    apRefExam, created = (getOrCreate(ApRefExam,toInsert=apRef,
                                        idAp=apRef.idAp,ciPaAp=apRef.ciPaAp,
                                        idExTaken=apRef.idExTaken,idEx=apRef.idEx,
                                        ciPaEx=apRef.ciPaEx))
                    if not created:
                        return recordAlreadyExists('apRefExam')
                elif request.method == 'PUT':
                    apRefExam, putted = (put(ApRefExam,toPut=apRef,
                                        idAp=apRef.idAp,ciPaAp=apRef.ciPaAp,
                                        idExTaken=apRef.idExTaken,idEx=apRef.idEx,
                                        ciPaEx=apRef.ciPaEx))
                    if not putted:
                        return recordDoesntExists('apRefExam')
                elif request.method == 'PATCH':
                    apRefExam, patched = (patch(ApRefExam,toPatch=apRef,
                                        idAp=apRef.idAp,ciPaAp=apRef.ciPaAp,
                                        idExTaken=apRef.idExTaken,idEx=apRef.idEx,
                                        ciPaEx=apRef.ciPaEx))
                    if not patched:
                        return recordDoesntExists('apRefExam')
                elif request.method == 'DELETE':
                    deleted = delete(ApRefExam,
                                     idAp=apRef.idAp,ciPaAp=apRef.ciPaAp,
                                     idExTaken=apRef.idExTaken,idEx=apRef.idEx,
                                     ciPaEx=apRef.ciPaEx)
                    if not deleted:
                        return recordDoesntExists('apRefExam')
        
        apRefTr = ApRefTr(idAp=apRefTrData['idAp'],
                          ciPaAp=apRefTrData['ciPaAp'],
                          idFollows=apRefTrData['idFollows'],
                          idTreatment=apRefTrData['idTreatment'],
                          ciPaTr=apRefTrData['ciPaAp'])

        suggestsTr = SuggestsTr(idAp=suggestsTrData['idAp'],
                                ciPaAp=suggestsTrData['ciPaAp'],
                                idTreatment=suggestsTrData['idTreatment'])

        requiresEx = RequiresEx(idAp=requiresExData['idAp'],
                                ciPaAp=requiresExData['ciPaAp'],
                                idEx=requiresExData['idExam'])

        fills = [Fills(idAp=fill['idAp'],ciPa=fill['ciPa'],
                       idForm=fill['idForm'], idQuestion=fill['idQuestion'],
                       response=fill['response']) for fill in fillsData]
        return recordCUDSuccessfully(tablename='patientApData',create=True)

    except Exception: # any other exception ocurred
        return provideData()