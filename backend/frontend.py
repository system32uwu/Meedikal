from flask import Blueprint, render_template

frontendRouter = Blueprint('app', __name__, url_prefix='/') # handles /app

@frontendRouter.route("/")
def frontend():
    return render_template('index.html')