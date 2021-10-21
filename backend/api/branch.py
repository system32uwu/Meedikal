from flask import Blueprint, request

from models.Branch import *
from util.crud import *
from middleware.authGuard import requiresRole, requiresAuth
from middleware.data import passJsonData, paginated

router = Blueprint('branch', __name__, url_prefix='/branch')

@router.get('/<int:id>') # GET /api/branch/<id>
@requiresAuth
def getBranchById(id:int, **kwargs):
    return crudReturn(Branch.getById(id))

@router.get('/<string:name>') # GET /api/branch/<name>
@requiresAuth
@paginated()
def getBranchByName(name:str, offset:int, limit:int, **kwargs):
    branches = Branch.filter({'name': {'value': name, 'operator': 'LIKE'}}, offset=offset, limit=limit)
    return crudReturn(branches)

@router.get('/all') # GET /api/branch/all
def getAllBranches():
    return crudReturn(Branch.query())

@router.post('/all') # POST /api/branch/all
@requiresAuth
@paginated()
def filterBranches(offset:int, limit:int, data:dict=None):
    return crudReturn(Branch.filter(data, offset=offset, limit=limit))

@router.post('') # POST /api/branch
@passJsonData
@requiresRole(['administrative'])
def createBranch(data:dict):
    return crudReturn(Branch(**data).save(data))

@router.route('', methods=['PUT', 'PATCH']) # PUT | PATCH /api/branch
@passJsonData
@requiresRole(['administrative'])
def updateBranch(data:dict):
    return crudReturn(Branch.update(data))

@router.route('/<int:id>', methods=['PUT', 'PATCH']) # PUT | PATCH /api/branch
@passJsonData
@requiresRole(['administrative'])
def updateBranchById(id:int, data:dict):
    return crudReturn(Branch.updateById(id, data))

@router.delete('') # DELETE /api/branch
@passJsonData
@requiresRole(['administrative'])
def deleteBranch(data:dict):
    return crudReturn(Branch.delete(data))

@router.route('/apTakesPlace', methods=['POST', 'PUT', 'PATCH', 'DELETE']) # POST | PUT | PATCH DELETE /api/branch/apTakesPlace
@passJsonData
@requiresRole(['administrative'])
def apTakesPlace(data:dict=None):
    if request.method == 'POST':
        return crudReturn(ApTakesPlace(**data).save(data))
    elif request.method == 'PUT' or request.method == 'PATCH':
        return crudReturn(ApTakesPlace.update(data))
    elif request.method == 'DELETE':
        return crudReturn(ApTakesPlace.delete(data))

@router.get('/apTakesPlace/<int:idAp>') # GET /api/branch/apTakesPlace/<idAp>
@requiresAuth
def getApTakesPlace(idAp:int):
    return crudReturn(ApTakesPlace.filter({'idAp': idAp}))