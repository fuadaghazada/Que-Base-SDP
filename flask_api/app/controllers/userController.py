from copy import deepcopy

from flask import Blueprint
from flask import jsonify
from flask import request

from app.models import User
from app.helpers.isAuth import isAuth

# Blue print
bluePrint = Blueprint('users', __name__, url_prefix='/users')
