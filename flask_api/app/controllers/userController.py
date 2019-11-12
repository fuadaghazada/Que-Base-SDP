from flask import Blueprint
from flask import jsonify
from flask import request

from app.models.user import User
from app.schemas.user import validateUser

# Blue print
bluePrint = Blueprint('users', __name__, url_prefix='/users')


'''
    [POST] Registering a user
'''

@bluePrint.route("/register", methods=["POST"])
def register():

    requestData = request.get_json()
    validation = validateUser(requestData)

    # Invalid
    if validation['success'] is False:
        return jsonify(validation)

    try:
        userData = validation['data']

        # New user
        user = User(userData)

        # Inserting
        status, msg = user.insert_one()

        # Response obj
        response = {
            "success": status,
            "message": msg
        }

        # Response
        return jsonify(response), 200

    except Exception as e:

        raise e

        # Response
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400


'''
    [POST] Logging a user
'''

@bluePrint.route("/login", methods=["POST"])
def login():

    requestData = request.get_json()
    validation = validateUser(requestData, True)

    # Invalid
    if validation['success'] is False:
        return jsonify(validation)

    try:
        # TODO: Login operations...
        pass

    except Exception as e:

        # Response
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400
