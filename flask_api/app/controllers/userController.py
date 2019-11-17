from flask import Blueprint
from flask import jsonify
from flask import request

from app.models.user import User
from app.schemas.user import validateUser
from app.utils.token import encode_token
from app.helpers.isAuth import isAuth

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
        })


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
        user = User.find_one(requestData['email'], requestData['password'])

        if user is None:
            return jsonify({
                "success": False,
                "message": "User not found"
            })

        # Generating a token with user data as payload
        token = encode_token(user)

        # Response
        return jsonify({
            "success": True,
            "message": "User is obtained successfully",
            "token": str(token)
        }), 200

    except Exception as e:

        raise e

        # Response
        return jsonify({
            "success": False,
            "message": str(e)
        })


'''
    [POST] Log out of the user
'''

@bluePrint.route("/logout", methods=["POST"])
@isAuth(request)
def logout(user):

    if user is not None:
        # Response
        return jsonify({
            "success": True,
            "message": "Successful logout"
        }), 200
    else:
        # Response
        return jsonify({
            "success": False,
            "message": "User not found"
        })
