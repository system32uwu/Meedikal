from flask import Blueprint
from middleware.data import passJsonData
from models import getTotal
from util.crud import crudReturn

router = Blueprint('pagination', __name__, url_prefix='/pagination')

@router.route('/total/<string:tablename>', methods=['GET', 'POST'])
@passJsonData
def totalOfTable(tablename:str, data:dict={}):
    return crudReturn(getTotal(tablename, data))