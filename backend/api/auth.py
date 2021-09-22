from middleware.authGuard import requiresAuth, requiresRole
from flask import Blueprint, request, make_response
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
        res = make_response(crudReturn(userToReturn(user)))

        res.set_cookie('authToken', token, httponly=True, samesite='Strict') # set the authToken as an httpOnly cookie (not accesible by javascript)

        return res, 200

@router.post('/me')
@requiresAuth
def me(ci:int):
    user = User.getByCi(ci)
    return crudReturn(userToReturn(user,request=request))

@router.post('/role')
@requiresRole('medicalPersonnel')
def role():
    return crudReturn(":D")

@router.post('/logout') # POST /api/auth/logout
def logout():
    res = make_response(crudReturn(True))
    res.delete_cookie('authToken') # remove the cookie, future TODO: implement blacklist system?
    return res, 200