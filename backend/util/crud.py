from typing import Any

from flask.json import jsonify
from .createDb import getDb

db = getDb()

def crudReturn(result:Any=None):
    return jsonify({"result": result}), 200