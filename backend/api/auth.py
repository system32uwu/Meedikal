from middleware.authGuard import requiresAuth, requiresRole
from flask import Blueprint, request, session
from models.User import User, AuthUser
from .user import userToReturn
from util.crud import crudReturn

router = Blueprint('auth', __name__, url_prefix='/auth')

@router.post('/login') # POST /api/auth/login
def login():
    data = request.get_json() # { 'ci' : 12345, 'password': contrasenaa }
    token, user = AuthUser.login(data['ci'], data['password'])

    if token is None:
        return {'error': 'incorrect CI or password'}, 400
    else:
        session['authToken'] = token
        return crudReturn(userToReturn(user))

@router.post('/logout') # POST /api/auth/logout
def logout():
    session.pop('authToken', None)
    return crudReturn(True)

@router.route('/me', methods=['POST', 'GET'])
@requiresAuth
def me(ci:int):
    user = User.getByCi(ci)
    return crudReturn(userToReturn(user,request=request))

@router.route('/updatePassword', methods=['PUT', 'PATCH'])
@requiresAuth
def updatePassword(ci:int):
    res = User.updatePassword(ci,request.get_json()['password'])
    return crudReturn(res)

@router.post('/roleExample') # example of route protected by role
@requiresRole('medicalPersonnel')
def role():
    return crudReturn("you have the correct role for this protected route!")