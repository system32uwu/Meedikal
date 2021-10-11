from flask import Blueprint, request

from models.Branch import *
from util.crud import *
from middleware.authGuard import requiresRole
from middleware.data import passJsonData

router = Blueprint('branch', __name__, url_prefix='/branch')

@router.get('/<int:id>') # GET /api/branch/<id>
def getBranchById(id:int):
    return crudReturn(Branch.getById(id))

@router.get('/<name>') # GET /api/branch/<name>
def getBranchByName(name:str=None):
    branches = Branch.filter({'name': name})
    return crudReturn(branches)

@router.get('/filter') # GET /api/branch/filter
@passJsonData
def getBranchByFilters(data:dict=None):
    branches = Branch.filter(data)
    return crudReturn(branches)

@router.get('/all') # GET /api/branch/all
def getAllBranches():
    return crudReturn(Branch.query())

@router.post('') # POST /api/branch
@passJsonData
@requiresRole('administrative')
def createBranch(data:dict):
    return crudReturn(Branch(**data).save(data))

@router.route('', methods=['PUT', 'PATCH']) # PUT | PATCH /api/branch
@passJsonData
@requiresRole('administrative')
def updateBranch(data:dict):
    return crudReturn(Branch.update(data))

@router.delete('') # DELETE /api/branch
@passJsonData
@requiresRole('administrative')
def deleteBranch(data:dict):
    return crudReturn(Branch.delete(data))

@router.route('/apTakesPlace', methods=['POST', 'PUT', 'PATCH', 'DELETE']) # POST | PUT | PATCH DELETE /api/branch/apTakesPlace
@passJsonData
@requiresRole('administrative')
def apTakesPlace(data:dict=None):
    if request.method == 'POST':
        return crudReturn(ApTakesPlace(**data).save(data))
    elif request.method == 'PUT' or request.method == 'PATCH':
        return crudReturn(ApTakesPlace.update(data))
    elif request.method == 'DELETE':
        return crudReturn(ApTakesPlace.delete(data))

@router.get('/apTakesPlace/<int:idAp>') # GET /api/branch/apTakesPlace/<idAp>
def getApTakesPlace(idAp:int):
    return crudReturn(ApTakesPlace.filter({'idAp': idAp}))