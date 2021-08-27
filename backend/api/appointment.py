from dataclasses import asdict
from flask import json, jsonify, Blueprint, request

from sqlalchemy import and_, or_

from util.crud import *
from util.returnMessages import *
from util.JSONEncoder import JsonExtendEncoder

from models.Appointment import Appointment

router = Blueprint('appointment', __name__, url_prefix='/appointment')

@router.route("/<int:id>", methods=['GET','DELETE'])
def hello(id):
    appointment = Appointment.query.filter(Appointment.id==id).first()

    if appointment is None:
        return recordDoesntExists("appointment")
    else:
        if request.method == 'GET':
            return jsonify(asdict(appointment)), 200
        else:
            appointment.delete()
            return recordCUDSuccessfully(delete=True)

@router.route("", methods=['POST', 'PUT', 'PATCH'])
def create_or_update():

    try:
        apData = json.loads(request.data)

        ap = Appointment(name=apData['name'], date=apData['date'],
                         state=apData['state'], timeBegins=apData['timeBegins'], 
                         timeEnds=apData['timeEnds'], etpp=apData['etpp'],
                         maxTurns=apData['maxTurns'])

        if request.method == 'POST':
            appointment, created = (get_or_create(model=Appointment, toInsert=ap, id=ap.id))
            if not created:
                return recordAlreadyExists()
            else:
                return recordCUDSuccessfully("appointment",create=True)

        if request.method == 'PUT' or request.method == 'PATCH': # add id
            ap.id = apData['id']

        if request.method == 'PUT':
            appointment, putted = (put(Appointment,ap,id=ap.id))
            if not putted:
                return recordDoesntExists()
            else:
                return recordCUDSuccessfully("user",update=True)
        elif request.method == 'PATCH':
            appointment, patched = (patch(Appointment,ap,id=ap.id))
            if not patched:
                return recordDoesntExists()
            else:
                return recordCUDSuccessfully("user",update=True)
    except:
        return provideData()