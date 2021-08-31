from flask import json, Blueprint, request

from models.Alert import * 
from util.crud import *

router = Blueprint('alert', __name__, url_prefix='/alert')

@router.route('/uHasAlert', methods=['POST','PUT','PATCH', 'GET', 'DELETE']) # /api/uHasAlert
def userHasAlert():
    if request.method == 'POST':
        data = json.loads(request.data)

        uHasAlert = data['uHasAlert']

        alerts = [getOrCreate(Alert, Alert(title=alert['title']), f"title = '{alert['title']}'") 
                                for alert in uHasAlert]
            
        for alert in alerts:
            for _d in uHasAlert:
                if _d['title'] == alert[0][0].title:
                    _d['idAlert'] = alert[0][0].id
                _d.pop('title', None)

        request.data = json.dumps({UHasAlert.__tablename__: uHasAlert})

    return crudv2(uHasAlert,request)