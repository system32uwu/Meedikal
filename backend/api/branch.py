from flask import Blueprint, request

from models.Branch import *
from util.crud import *
from middleware.data import passJsonData

router = Blueprint('branch', __name__, url_prefix='/branch')

@router.get('/<int:id>') # GET /api/branch/<id>
def getBranchById(id:int):
    return crudReturn(Branch.getById(id))

@router.get('/<name>') # GET /api/branch/<name>
@router.post('/filter') # POST /api/branch/filter
@passJsonData
def getBranchByFilters(name:str=None, data:dict=None):
    if request.method == 'POST':
        branches = Branch.filter(data)
    else:
        branches = Branch.filter({'name': name})
    return crudReturn(branches)

@router.get('/all') # GET /api/branch/all
def getAllBranches():
    return crudReturn(Branch.query())

@router.post('') # POST /api/branch
@passJsonData
def createBranch(data:dict):
    return crudReturn(Branch(**data).save(data))

@router.route('', methods=['PUT', 'PATCH']) # PUT | PATCH /api/branch
@passJsonData
def updateBranch(data:dict):
    return crudReturn(Branch.update(data))

@router.delete('') # DELETE /api/branch
@passJsonData
def deleteBranch(data:dict):
    return crudReturn(Branch.delete(data))

@router.route('/apTakesPlace', methods=['POST', 'PUT', 'PATCH', 'DELETE']) # POST | PUT | PATCH DELETE /api/branch/apTakesPlace
@router.get('/apTakesPlace/<int:idAp>') # GET /api/branch/apTakesPlace/<idAp>
@passJsonData
def apTakesPlace(idAp:int=None, data:dict=None):
    if request.method == 'POST':
        return crudReturn(ApTakesPlace(**data).save(data))
    if request.method == 'PUT' or request.method == 'PATCH':
        return crudReturn(ApTakesPlace.update(data))
    if request.method == 'DELETE':
        return crudReturn(ApTakesPlace.delete(data))
    elif request.method == 'GET':
        return crudReturn(ApTakesPlace.filter({'idAp': idAp}))