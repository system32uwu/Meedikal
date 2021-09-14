from dataclasses import asdict
from flask import Blueprint, request

from models.Branch import *
from util.crud import *

router = Blueprint('branch', __name__, url_prefix='/branch')

@router.get('/<int:id>') # GET /api/branch/<id>
def getBranchById(id:int):
    b = Branch.getById(id)
    return crudReturn(asdict(b))

@router.get('/<name>') # GET /api/branch/<name>
@router.post('/name') # POST /api/branch/name # could be just name or other params like location as well
def getBranchByName(name:str=None):
    if request.method == 'POST':
        branches = Branch.filter(request.get_json())
    else:
        branches = Branch.filter({'name': name})
    return crudReturn([asdict(b) for b in branches])

@router.get('/all') # GET /api/branch/all
def getAllBranches():
    return crudReturn([asdict(b) for b in Branch.query()])

@router.post('') # POST /api/branch
def createBranch():
    b = Branch(**request.get_json()).save()
    return crudReturn(asdict(b))

@router.route('', methods=['PUT', 'PATCH']) # PUT | PATCH /api/branch
def updateBranch():
    branches = Branch.update(request.get_json())
    return crudReturn([asdict(b) for b in branches])

@router.delete('') # DELETE /api/branch
def deleteBranch():
    b = Branch.delete(request.get_json())
    return crudReturn(b)

@router.route('/apTakesPlace', methods=['POST', 'PUT', 'PATCH', 'GET', 'DELETE']) # POST | PUT | PATCH | GET | DELETE /api/branch/apTakesPlace
def apTakesPlace():
    data = request.get_json()
    if request.method == 'POST':
        return crudReturn(asdict(ApTakesPlace(**data).save()))
    if request.method == 'PUT' or request.method == 'PATCH':
        return crudReturn([asdict(aptp) for aptp in ApTakesPlace.update(data)])
    if request.method == 'DELETE':
        return crudReturn(ApTakesPlace.delete(data))
    elif request.method == 'GET':
        return crudReturn([asdict(aptp) for aptp in ApTakesPlace.filter(data)])