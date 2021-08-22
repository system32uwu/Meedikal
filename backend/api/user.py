from flask import jsonify, Blueprint, request
from models.User import User
router = Blueprint('user', __name__, url_prefix='/user')

@router.route('', methods=['GET']) # GET /api/user
def allUsers():
    return jsonify(User.query.all())

@router.route('', methods=['POST']) # POST /api/user
def userByCi():
    ci = request.form['ci'] # enviado desde postman como form-data
    print(f'ci es: {ci}')
    return jsonify(User.query.filter(User.ci == ci).first())