from flask import Blueprint, render_template
from config import Config
from models.User import User
from middleware.authGuard import getCurrentRole, requiresRole
from api.user import userToReturn

appRouter = Blueprint('app', __name__, url_prefix='app') # handles /app

@appRouter.get('')
@appRouter.get('/')
@getCurrentRole
def home(currentRole:str, *args, **kwargs):
    return render_template(f'pages/app/{currentRole}/home.html')

@appRouter.get('/profile')
@getCurrentRole
def profile(currentRole:str, ci:int):
    user = userToReturn(User.getByCi(ci), currentRole)
    return render_template(f'pages/app/{currentRole}/profile.html', user=user)

@appRouter.get('/appointments')
@getCurrentRole
def appointments(currentRole:str, *args, **kwargs):
    return render_template(f'pages/app/{currentRole}/appointments.html')

@appRouter.get('/symptoms')
@getCurrentRole
def symptoms(currentRole:str, *args, **kwargs):
    return render_template(f'pages/app/{currentRole}/symptoms.html')

@appRouter.get('/clinical-signs')
@getCurrentRole
def clinicalSigns(currentRole:str, *args, **kwargs):
    return render_template(f'pages/app/{currentRole}/clinical-signs.html')

@appRouter.get('/diseases')
@getCurrentRole
def diseases(currentRole:str, *args, **kwargs):
    return render_template(f'pages/app/{currentRole}/diseases.html')

@appRouter.get('/branches')
@getCurrentRole
def branches(currentRole:str, *args, **kwargs):
    return render_template(f'pages/app/{currentRole}/branches.html')


@appRouter.get('/settings')
@getCurrentRole
def settings(*args, **kwargs):
    return render_template('pages/app/public/index.html')

# mp specifics
@appRouter.get('/patients')
@requiresRole(['medicalPersonnel'])
def patients():
    return render_template(f'pages/app/mp/patients.html')

# admin specifics
@appRouter.get('/users')
@requiresRole(['administrative'])
def users():
    return render_template(f'pages/app/administrative/users.html')

@appRouter.get('/stats')
@requiresRole(['administrative'])
def stats():
    return render_template(f'pages/app/administrative/stats.html')

@appRouter.context_processor
@getCurrentRole
def appVars(currentRole:str, ci:int):
    return dict(currentRole=currentRole, ci=ci, app_pages=Config.app_pages)