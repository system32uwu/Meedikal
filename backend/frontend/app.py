from flask import Blueprint, render_template, request
from config import Config
from models.User import User
from models.Appointment import Appointment, AssignedTo
from middleware.authGuard import getCurrentRole, requiresRole, requiresAuth
from api.user import userToReturn
from datetime import date
appRouter = Blueprint('app', __name__, url_prefix='app') # handles /app

baseDir = 'pages'
baseDirApp = f'{baseDir}/app'

@appRouter.get('')
@appRouter.get('/')
@requiresAuth
def home(**any):
    return render_template(f'{baseDirApp}/home.html')

@appRouter.get('/profile')
@getCurrentRole
def profile(ci:int, currentRole:str):
    user = userToReturn(User.getByCi(ci), currentRole)
    return render_template(f'{baseDirApp}/profile.html', me=user)

@appRouter.get('/profile/<int:ciUser>')
@appRouter.get('/profile/<int:ciUser>/<string:asRole>')
@requiresAuth
def profileById(ciUser:int, asRole:str=None, *args, **kwargs):
    user = userToReturn(User.getByCi(ciUser), asRole)
    return render_template(f'{baseDirApp}/profile.html', user=user)

@appRouter.get('/appointments')
@requiresAuth
def appointments(**any):
    return render_template(f'{baseDirApp}/appointments.html')

@appRouter.get('/appointment/<int:id>')
@requiresAuth
def appointmentById(id:int, **any):
    ap = Appointment.getById(id)
    ciDoc = AssignedTo.filter({'idAp': ap.id}, 'one')
    
    doctor = userToReturn(User.getByCi(ciDoc))
    
    return render_template(f'{baseDirApp}/appointment.html', appointment=ap, doctor=doctor)

@appRouter.get('/symptoms')
@requiresAuth
def symptoms(**any):
    return render_template(f'{baseDirApp}/symptoms.html')

@appRouter.get('/clinical-signs')
@requiresAuth
def clinicalSigns(**any):
    return render_template(f'{baseDirApp}/clinical-signs.html')

@appRouter.get('/diseases')
@requiresAuth
def diseases(**any):
    return render_template(f'{baseDirApp}/diseases.html')

@appRouter.get('/branches')
def branches():
    return render_template(f'{baseDir}/branches.html')

@appRouter.get('/settings')
@requiresAuth
def settings(**any):
    return render_template(f'{baseDirApp}/settings.html')

# mp specifics
@appRouter.get('/patients')
@requiresRole(['medicalPersonnel'])
def patients():
    return render_template(f'{baseDirApp}/mp/patients.html')

@appRouter.get('/users')
@requiresRole(['administrative'])
def users():
    return render_template(f'{baseDirApp}/administrative/users.html')

@appRouter.get('/create-user')
@requiresRole(['administrative'])
def createUser():
    return render_template(f'{baseDirApp}/administrative/create-user.html')

@appRouter.get('/update-user/<int:ciUser>')
@requiresRole(['administrative'])
def updateUser(ciUser:int):
    user = userToReturn(User.getByCi(ciUser))
    return render_template(f'{baseDirApp}/administrative/update-user.html', user=user)

@appRouter.get('/stats')
@requiresRole(['administrative'])
def stats():
    return render_template(f'{baseDirApp}/administrative/stats.html')

@appRouter.context_processor
@getCurrentRole
def appVars(ci:int, currentRole:str):
    url = request.url.split('/app', 1)[1]
    if url == '/':
        url = 'home'
    else:
        url = url.split('/')[1]
        url = url.replace('-', ' ')

    return dict(myRole=currentRole, ci=ci, 
    appPages=Config.app_pages, roleColors=Config.role_colors,
    currentPage=url.capitalize(), currentDate = date.today())