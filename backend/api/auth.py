from util.authGuard import requiresAuth, requiresRole
from util.crud import crudReturn
from .user import userToReturn
from flask import Blueprint, request, make_response
from models.User import AuthUser
import jwt

router = Blueprint('auth', __name__, url_prefix='/auth')

@router.errorhandler(jwt.ExpiredSignatureError)
def expiredToken():
    return {'error': 'Signature expired. Please log in again.'}, 401

@router.errorhandler(jwt.InvalidTokenError)
def invalidToken():
    return {'error': 'Invalid token. Please log in again.'}, 401
# example of protected route, which requires the user to have the medicalPersonnel role
@router.post('/protectedRoute') 
@requiresAuth
@requiresRole('medicalPersonnel')
def protectedRouteWithMedicalPersonnelRoleRequired():
    return {"result": "allowed"}, 200

# example of protected route
@router.post('/protectedRoute') 
@requiresAuth
def protectedRoute():
    return {"result": "you're authenticated :)!"}, 200

@router.post('/login') # POST /auth/login
def login():
    data = request.get_json()
    u = AuthUser(data['ci'], data['password']) # { 'ci' : 12345, 'password': contrasenaa }
    success = u.login()

    if not success:
        return {'error': 'incorrect CI or password'}, 400
    else:
        token = u.issueAuthToken()

        res = make_response(crudReturn(userToReturn(u.user)))

        res.set_cookie('authToken', token, httponly=True, samesite='Strict') # set the authToken as an httpOnly cookie (not accesible by javascript)
        
        return res, 200

@router.post('/logout') # POST /auth/logout
def logout():
    res = make_response(crudReturn(True))
    res.delete_cookie('authToken') # remove the cookie, future TODO: implement blacklist system?        
    return res, 200