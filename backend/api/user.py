from flask import json, jsonify, Blueprint, request
from models.User import User

router = Blueprint('user', __name__, url_prefix='/user')

@router.route('/all', methods=['GET']) # GET /api/user/all
def allUsers():
    return jsonify(User.query.all()), 200

@router.route('/<int:ci>', methods=['GET']) # GET /api/user/1
def userByCi(ci):
    return jsonify(User.query.filter(User.ci == ci).first())