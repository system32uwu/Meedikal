from flask import Blueprint, request

from models.Vaccine import *
from util.crud import *

router = Blueprint('vaccine', __name__, url_prefix='/vaccine')

@router.route('',  methods=['POST','PUT','PATCH', 'GET', 'DELETE'])
def vaccine():
    return crudv2(Vaccine,request)

@router.get('/name')
def getVaccineByName():
    data = json.loads(request.data)
    vaccines = Vaccine.query.filter(Vaccine.name.contains(data['vaccine']['name'])).all()
    return crudv2(request=request,preparedResult=[asdict(_vaccine) for _vaccine in vaccines])

@router.route('/uTakesVaccine', methods=['POST','PUT','PATCH', 'GET', 'DELETE']) # /api/uTakesVaccine
def uTakesVaccine():
    return crudv2(UTakesVaccine,request)