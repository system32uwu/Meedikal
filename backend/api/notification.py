from flask import Blueprint, request

from models.Notification import *
from util.crud import *

router = Blueprint('notification', __name__, url_prefix='/notification')

@router.route('',  methods=['POST','PUT','PATCH', 'GET', 'DELETE'])
def notification():
    return crudv2(Notification,request)

@router.route('/uReceivesNot',  methods=['POST','PUT','PATCH', 'GET', 'DELETE'])
def uReceivesNotification():
    if request.method == 'POST':
        data = json.loads(request.data)

        uReceivesNot = data['uReceivesNot']

        notifications = [getOrCreate(Notification, Notification(title=notification['title'],date=notification['date'],content=['content'])) 
                        for notification in uReceivesNot]
            
        for notification in notifications:
            for _d in uReceivesNot:
                if _d['title'] == notification[0][0].title:
                    _d['idNot'] = notification[0][0].id
                _d.pop('title', None)
                _d.pop('content', None)
                _d.pop('date', None)

        request.data = json.dumps({UReceivesNot.__tablename__: uReceivesNot})
    
    return crudv2(UReceivesNot,request)
