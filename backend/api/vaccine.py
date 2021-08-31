from flask import Blueprint, request

from models.Vaccine import *
from util.crud import *

router = Blueprint('vaccine', __name__, url_prefix='/vaccine')

@router.route('',  methods=['POST','PUT','PATCH', 'GET', 'DELETE'])
def vaccine():
    return crudv2(Vaccine,request)

@router.route('/uTakesVaccine', methods=['POST','PUT','PATCH', 'GET', 'DELETE']) # /api/uTakesVaccine
def uTakesVaccine():
    return crudv2(UTakesVaccine,request)