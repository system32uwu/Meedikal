from flask import Blueprint

from models.ClinicalSign import ClinicalSign
from models.Disease import Disease
from models.Symptom import Symptom
from util.crud import *
from middleware.authGuard import requiresRole, requiresAuth
from middleware.data import paginated, passJsonData

router = Blueprint('suffering', __name__, url_prefix='/suffering')

@router.route('/search/<string:sufferingType>', methods=['GET','POST'])
@requiresAuth
@paginated()
def searchSuffering(sufferingType:str, offset:int, limit:int, data:dict={}, **kw):
    result = []

    if sufferingType == 'disease':
        result = Disease.filter(data, 'OR', offset=offset, limit=limit) or []
    elif sufferingType == 'symptom':
        result = Symptom.filter(data, 'OR', offset=offset, limit=limit) or []
    elif sufferingType == 'clinicalSign':
        result = ClinicalSign.filter(data, 'OR', offset=offset, limit=limit) or []

    if len(result) > 0:
        for r in result:
            if r.description is not None:
                r.description = r.description[:15] + '..' * (len(r.description) > 15)

        result = [asdict(r) for r in result]

    return crudReturn(result)

@router.post('/<string:sufferingType>')
@requiresRole(['doctor', 'administrative'])
@passJsonData
def createSuffering(sufferingType:str, data:dict={}):
    result = None

    if sufferingType == 'disease':
        result = Disease(**data).save(data)
    elif sufferingType == 'symptom':
        result = Symptom(**data).save(data)
    elif sufferingType == 'clinicalSign':
        result = ClinicalSign(**data).save(data)

    return crudReturn(result)

@router.route('/<string:sufferingType>', methods=['PUT', 'PATCH'])
@requiresRole(['doctor', 'administrative'])
@passJsonData
def updateSuffering(sufferingType:str, data:dict={}):
    result = None

    if sufferingType == 'disease':
        result = Disease.update(data)
    elif sufferingType == 'symptom':
        result = Symptom.update(data)
    elif sufferingType == 'clinicalSign':
        result = ClinicalSign.update(data)
        
    return crudReturn(result)

@router.delete('/<string:sufferingType>')
@requiresRole(['doctor', 'administrative'])
@passJsonData
def deleteSuffering(sufferingType:str, data:dict={}):
    result = None
    if sufferingType == 'disease':
        result = Disease.delete(data)
    elif sufferingType == 'symptom':
        result = Symptom.delete(data)
    elif sufferingType == 'clinicalSign':
        result = ClinicalSign.delete(data)
        
    return crudReturn(result)