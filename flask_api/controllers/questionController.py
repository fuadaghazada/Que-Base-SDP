from flask import Blueprint
from flask import jsonify
from flask import request

from models.question import Question
from schemas.question import validateQuestion
from helpers.operateDb import findSimilarQuestions

# Blue print
bluePrint = Blueprint('questions', __name__, url_prefix='/questions')

'''
    [GET] Retrieving similar questions with request
'''

@bluePrint.route("/findSimilarQuestions", methods=["GET"])
def getSimilarQuestions():

    requestData = request.get_json()

    # Error in parameters
    if "questionBody" not in dict(requestData):
        # Response
        return jsonify({
            'success': False,
            "message": "Please provide the 'questionBody' field in the body"
        }), 400

    # Extracting question body from the request
    questionBody = requestData['questionBody']

    # Finding process...
    foundQuestions = findSimilarQuestions(questionBody)

    # Response
    return jsonify({
        'success': True,
        "results": foundQuestions
    }), 200


'''
    [POST] Inserting a question with request
'''

@bluePrint.route("/insertQuestion", methods=["POST"])
def postInsertQuestion():

    requestData = request.get_json()
    validation = validateQuestion(requestData)

    # Invalid
    if validation['success'] is False:
        return jsonify(validation)

    try:
        # Inserting
        status, msg = Question(requestData["body"]).insert_one()

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
        }), 400
