from util.JSONEncoder import JsonExtendEncoder
from flask import Flask, Blueprint, render_template

from config import DevelopmentConfig

from api.router import apiRouter

frontendRouter = Blueprint('app', __name__, url_prefix='/app') # handles /app

@frontendRouter.route("/")
def frontend():
    return render_template('index.html')

def create_app() -> Flask:
    app = Flask(__name__, static_folder='../frontend/build/static', template_folder='../frontend/build') # serve compiled react app.

    app.config.from_object(DevelopmentConfig)

    # --- CUSTOM
    app.json_encoder = JsonExtendEncoder

    # --- ROUTERS
    app.register_blueprint(apiRouter) # api
    app.register_blueprint(frontendRouter) # frontend
    # --- ROUTERS

    return app

if __name__ == '__main__':
    create_app().run()