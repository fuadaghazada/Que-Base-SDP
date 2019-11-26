from copy import deepcopy

from flask import Blueprint
from flask import jsonify
from flask import request

from app.models.question import Question
from app.helpers.isAuth import isAdmin
from app.utils.readQuestions import readQuestions

# Blue print
bluePrint = Blueprint('admin', __name__, url_prefix='/admin')


'''
    [POST] Inserting a question with request
'''

@bluePrint.route("/insertQuestion", methods=["POST"])
@isAdmin(request)
def postInsertQuestion():

    requestData = request.get_json()
    
    # Error in parameters
    if "filename" not in dict(requestData):
        # Response
        return jsonify({
            'success': False,
            "message": "Please provide the 'filename' field in the body"
        })

    filename = requestData['filename']

    # Other question propertiess
    questionObj = deepcopy(requestData)
    del questionObj["filename"]

    # Reading the questions from the given file
    questions = readQuestions(filename)

    try:
        for question in questions:
            questionObj["body"] = question

            status, msg = Question(questionObj).insert_one()
            print(f"-- {msg} ---")
            break


        return jsonify({
            "success": True,
            "message": "Questions are obtained!"
        })

    except Exception as e:

        # Response
        return jsonify({
            "success": False,
            "message": str(e)
        })
