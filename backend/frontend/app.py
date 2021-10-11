from flask import Blueprint, render_template, session
from middleware.authGuard import getCurrentRole, requiresAuth, requiresRole
from models.User import User

appRouter = Blueprint('app', __name__, url_prefix='app') # handles /app

@appRouter.get('')
@appRouter.get('/')
@getCurrentRole
def home(ci:int, currentRole:str):
    if not currentRole:
        currentRole = User.getRoles(ci)[0]
        session['currentRole'] = currentRole
    
    return render_template(f'pages/app/{currentRole}/home.html')