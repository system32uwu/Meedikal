from flask import Blueprint
from middleware.data import passJsonData
from models import BaseModel
from util.crud import crudReturn

router = Blueprint('pagination', __name__, url_prefix='/pagination')

@router.get('/total/<string:tablename>')
@passJsonData
def getTotal(tablename:str, data:dict=None):
    _module = __import__('models')
    _class: BaseModel = getattr(_module, tablename.capitalize())
        
    total = _class.filter(data, paginationOnly=True)
        
    return crudReturn(total)