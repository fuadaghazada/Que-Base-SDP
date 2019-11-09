from flask import Blueprint
from flask import jsonify
from flask import request
from flask import redirect
from flask import url_for

from db import getDb
from helpers.operateDb import findSimilarQuestions, insertQuestion
from utils.JSONEncoder import customEncode

# Blue print
bluePrint = Blueprint('questions', __name__, url_prefix='/questions')

'''
    [GET] Retrieving similar questions with request
'''

@bluePrint.route("/findSimilarQuestions", methods=["GET"])
def getSimilarQuestions():

    # DB
    db = getDb()
    requestData = request.json

    # Error in DB
    if db is None:
        return jsonify({
            'success': False,
            'message' : 'DB connection cannot be established'
        })

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
    foundQuestions = findSimilarQuestions(questionBody, db)

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

    # DB
    db = getDb()
    requestData = request.json

    # Error in DB
    if db is None:
        return jsonify({
            'success': False,
            'message' : 'DB connection cannot be established'
        })

    try:
        # Inserting
        status, msg = insertQuestion(requestData, db)

        # Response obj
        response = {
            "status": status,
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
            "message": str(e)
        })
