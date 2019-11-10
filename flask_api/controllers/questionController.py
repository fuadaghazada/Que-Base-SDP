from flask import Blueprint
from flask import jsonify
from flask import request
from flask import redirect
from flask import url_for

from db import getDb
from models.question import Question

from helpers.operateDb import findSimilarQuestions
from utils.JSONEncoder import customEncode

# Blue print
bluePrint = Blueprint('questions', __name__, url_prefix='/questions')

'''
    [GET] Retrieving similar questions with request
'''

@bluePrint.route("/findSimilarQuestions", methods=["GET"])
def getSimilarQuestions():

    requestData = request.json

    # Error in parameters
    if "questionBody" not in dict(requestData):
        # Response
        return jsonify({
            'success': False,
            "message": "Please provide the 'questionBody' field in the body"
        })

    # Extracting question body from the request
    questionBody = requestData['questionBody']

    # Finding process...
    foundQuestions = findSimilarQuestions(questionBody)

    # Response
    return jsonify({
        'success': True,
        "results": customEncode(foundQuestions)
    })


'''
    [POST] Inserting a question with request
'''

@bluePrint.route("/insertQuestion", methods=["POST"])
def postInsertQuestion():

    requestData = request.json

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
        return jsonify(response)

    except Exception as e:

        # Response
        return jsonify({
            "success": False,
            "message": str(e)
        })
