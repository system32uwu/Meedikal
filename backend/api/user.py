from flask import json, jsonify, Blueprint, request
from models.User import User
router = Blueprint('user', __name__, url_prefix='/user')

@router.route('', methods=['GET']) # GET /api/user
def allUsers():
    return jsonify(User.query.all())

@router.route('', methods=['POST']) # POST /api/user
def userByCi():
    try:
        userData = json.loads(request.data)
        ci = userData['ci']
        return jsonify(User.query.filter(User.ci == ci).first())   
    except:
        return 'missing ci', 400 # if there was no request.data or userData['ci], return this.