from copy import deepcopy

from flask import Blueprint
from flask import jsonify
from flask import request

from app.models import User
from app.helpers.isAuth import isAuth

# Blue print
bluePrint = Blueprint('users', __name__, url_prefix='/users')

@bluePrint.route("/getUser", methods=["GET"])
@isAuth(request)
def getUser(user):

    # ID as parameter
    userId = request.args.get('id')

    result = None
    try:
        result = User({"_id": userId}).data()
    except Exception as e:
        print("NO SUCH USER ID")

    status = result is not None

    # Return the response
    return jsonify({
        'success': status,
        "user": result
    }), 200
