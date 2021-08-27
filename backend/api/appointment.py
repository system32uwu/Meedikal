from dataclasses import asdict
from flask import json, jsonify, Blueprint, request

from sqlalchemy import and_, or_

from util.crud import *
from util.returnMessages import *

router = Blueprint('appointment', __name__, url_prefix='/appointment')

@router.route("/")
def hello():
    return "world"