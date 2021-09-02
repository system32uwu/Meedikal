from flask import json, Blueprint, request

from models.Form import * 
from util.crud import *

router = Blueprint('form', __name__, url_prefix='/form')

@router.route('', methods=['POST','PUT','PATCH', 'GET', 'DELETE']) # /api/form
def form():
    return crudv2(Form,request)

@router.route('/designed', methods=['POST','PUT','PATCH', 'GET', 'DELETE']) # /api/form/designed
def designed():
    return crudv2(Form,request)

router.route('/from', methods=['POST','PUT','PATCH', 'GET', 'DELETE']) #/api/form/from
def questionFromForm():
    if request.method == 'POST':
        data = json.loads(request.data)

        _from = data['from']

        questions = [getOrCreate(Question, Question(text=q['text']), f"text = '{q['text']}'") 
                                for q in _from]
            
        for q in questions:
            for _d in _from:
                if _d['text'] == q[0][0].text:
                    _d['idQ'] = q[0][0].id
                _d.pop('text', None)

        request.data = json.dumps({From.__tablename__: From})

    return crudv2(From,request)