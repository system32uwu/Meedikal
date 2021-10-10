from flask import Blueprint, session
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

@router.post('/roleExample') # example of route protected by role
@requiresRole('medicalPersonnel')
def role():
    return crudReturn("you have the correct role for this protected route!")