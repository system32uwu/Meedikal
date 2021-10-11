from flask import Blueprint, session, request
from middleware.data import passJsonData
from middleware.authGuard import requiresAuth, requiresRole
from models.User import User, AuthUser
from .user import userToReturn
from util.crud import crudReturn
from util.returnMessages import genericErrorReturn

router = Blueprint('auth', __name__, url_prefix='/auth')

@router.post('/login') # POST /api/auth/login
@passJsonData
def login(data:dict):
    token = AuthUser.login(data['ci'], data['password'])

    if token is None:
        return genericErrorReturn('incorrect CI or password')
    else:
        session['authToken'] = token
        return crudReturn('OK')

@router.post('/logout') # POST /api/auth/logout
def logout():
    session.pop('authToken', None)
    return crudReturn('OK')

@router.route('/me', methods=['POST', 'GET']) # POST /api/auth/me
@requiresAuth
def me(ci:int):
    user = User.getByCi(ci)
    return crudReturn(userToReturn(user))

@router.route('/updatePassword', methods=['PUT', 'PATCH']) # POST /api/auth/updatePassword
@requiresAuth
@passJsonData
def updatePassword(ci:int,data:dict):
    res = User.updatePassword(ci,data['password'])
    return crudReturn(res)

@router.route('/currentRole', methods=['GET', 'POST'])
def currentRole():
    @requiresRole(request.get_json()['role']) # to change to the desired role, the user should have it already
    def withinFlaskContext():
        if request.method == 'POST':
            session['currentRole'] = request.get_json()['role']
        else:
            return crudReturn(session['currentRole'])
    return withinFlaskContext()