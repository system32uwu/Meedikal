from flask.templating import render_template
from util.JSONEncoder import JsonExtendEncoder
from flask import Flask

from config import DevelopmentConfig

from api.router import apiRouter
from frontend import frontendRouter

app = Flask(__name__, static_folder='build/static', template_folder='build')

app.config.from_object(DevelopmentConfig)

# --- CUSTOM
app.json_encoder = JsonExtendEncoder

# --- ROUTERS
app.register_blueprint(apiRouter) # api
app.register_blueprint(frontendRouter) # frontend
# --- ROUTERS

# @app.errorhandler(404) # whatever produces a 404, redirect to index 
# def handler(*args):
#     return render_template('index.html')

if __name__ == '__main__':
    app.run()