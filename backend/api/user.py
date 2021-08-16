from flask import jsonify, Blueprint

router = Blueprint('user', __name__, url_prefix='/user')

@router.route('/', methods=['GET'])
def allUsers():
    return {"hello": "world"}