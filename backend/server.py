from flask import Flask

from config import DevelopmentConfig
from routers import apiRouter, frontendRouter
import errorhandlers
from util.JSONEncoder import JsonExtendEncoder

app = Flask(__name__, static_folder='build/static', template_folder='build')

app.config.from_object(DevelopmentConfig)

# --- CUSTOM ENCODER (used to encode dates)
app.json_encoder = JsonExtendEncoder

# --- MAIN ROUTERS
app.register_blueprint(apiRouter) # api
app.register_blueprint(frontendRouter) # frontend
# --- MAIN ROUTERS

if __name__ == '__main__':
    app.run()