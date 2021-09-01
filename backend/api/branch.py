from flask import Blueprint, request

from models.Branch import *
from util.crud import *

router = Blueprint('branch', __name__, url_prefix='/branch')

@router.route('', methods=['POST','PUT','PATCH','GET','DELETE'])
def branch():
    return crudv2(Branch,request)

@router.get('/all')
def getAllBranches():
    return crudv2(request=request,preparedResult=[asdict(b) for b in Branch.query.all()])

@router.route('/apTakesPlace', methods=['POST','PUT','PATCH','GET','DELETE'])
def branch():
    return crudv2(ApTakesPlace,request)

@router.route('/trTakesPlace', methods=['POST','PUT','PATCH','GET','DELETE'])
def branch():
    return crudv2(TrTakesPlace,request)