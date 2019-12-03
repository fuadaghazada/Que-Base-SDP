from bson.objectid import ObjectId

from flask import Blueprint
from flask import jsonify
from flask import request

from app.models import Question, User

from app.schemas import validateQuestion, validateFilterQuery

from app.helpers.isAuth import isAuth
from app.helpers.filter import createFilterQuery


# Blue print
bluePrint = Blueprint('questions', __name__, url_prefix='/questions')


'''
    [POST] Inserting a question with request
'''

@bluePrint.route("/insertQuestion", methods=["POST"])
@isAuth(request)
def postInsertQuestion(user):

    requestData = request.get_json()
    validation = validateQuestion(requestData)

    # Invalid
    if validation['success'] is False:
        return jsonify(validation)

    try:
        # Inserting
        requestData['userId'] = user["_id"]
        status, msg = Question(requestData).insert_one()

        # Response obj
        response = {
            "success": status,
            "message": msg
        }

        # Checking the status of insertion
        if status is True:
            response["question"] = requestData

        # Response
        return jsonify(response), 200

    except Exception as e:

        # Response
        return jsonify({
            "success": False,
            "message": str(e)
        })


'''
    [POST] Getting the questions by filtering according to the fields
'''

@bluePrint.route("/getQuestions", methods=["POST"])
@isAuth(request)
def getQuestions(user):

    # Get the request and validate it
    requestData = request.get_json()

    validation = validateFilterQuery(requestData)

    # Parameters
    page = int(request.args.get('page')) if request.args.get('page') is not None else 1

    if validation['success'] is False:
        return jsonify(validation)

    # Creating the filter query
    filterData, message = createFilterQuery(requestData)
    if filterData:
        queryDict, sortingAttr, sortOrder = filterData

        # Sending the query...
        results = Question.find(queryDict, sortingAttr, sortOrder, page)

        # Return the response
        return jsonify({
            'success': True,
            "questions": results,
            "message": message
        }), 200

    # Return the response
    return jsonify({
        'success': False,
        "message": message
    }), 200


'''
    [POST] Favorite/disfavorite a question given its id
'''

@bluePrint.route("/favoriteQuestion", methods=["POST"])
@isAuth(request)
def favoriteQuestion(user):

    # Question ID as parameter & userID from header
    questionId = request.args.get('id')
    userId = user["_id"]

    # Getting the user adding the favorite questions to list
    user = User({"_id": userId})
    status, message = user.favoriteQuestion(questionId)

    # Return the response
    return jsonify({
        'success': True,
        'result': status,
        'message': message
    }), 200


'''
    [GET] Getting a question according to its id
'''

@bluePrint.route("/getQuestion", methods=["GET"])
@isAuth(request)
def getQuestion(user):

    # ID as parameter
    questionId = request.args.get('id')

    result = None
    try:
        result = Question({"_id": questionId}).data()
    except Exception as e:
        print("NO SUCH QUESTION ID")

    status = result is not None

    # Return the response
    return jsonify({
        'success': status,
        "question": result
    }), 200
