from flask import Blueprint
from flask import jsonify
from flask import request

from app.models.question import Question
from app.models.searchCache import SearchedQuestion
from app.schemas.question import validateQuestion
from app.schemas.questionQuery import validateQuestionQuery
from app.helpers.operateDb import findSimilarQuestions
from app.helpers.operateDb import filterQuestionsByAttributes
from app.helpers.isAuth import isAuth
from app.helpers.constant import MIN_THRESHOLD


# Blue print
bluePrint = Blueprint('questions', __name__, url_prefix='/questions')

'''
    [GET] Retrieving similar questions with request
'''

@bluePrint.route("/findSimilarQuestions", methods=["GET"])
@isAuth(request)
def getSimilarQuestions(user):

    requestData = request.get_json()
    validation = validateQuestion(requestData)

    # Parameters
    threshold = int(request.args.get('threshold')) if request.args.get('threshold') is not None else MIN_THRESHOLD
    page = int(request.args.get('page')) if request.args.get('page') is not None else 1

    # Invalid
    if validation['success'] is False:
        return jsonify(validation)

    # Extracting question body from the request
    questionBody = requestData['body']

    # Questions response list
    questions = []

    searchedQuestion = SearchedQuestion(requestData)
    if not searchedQuestion.check_exists():
        # Finding process...
        foundQuestions = findSimilarQuestions(questionBody)

        if foundQuestions:
            questionsData = list(map(lambda x: {"questionId": x['question']['_id'], "similarityRate": x['similarity_rate']}, foundQuestions))

            searchedQuestion.setCacheData(questionsData)
            searchedQuestion.insert_one()
        else:
            # Response
            return jsonify({
                'success': False,
                "message": "Analyze is not successful"
            })

    # Result questions
    results = searchedQuestion.get(threshold, page)
    questions = results["data"]
    questions.sort(key = lambda x: x['similarityRate'])

    # Updating the results in dict
    results["data"] = questions

    # Response
    return jsonify({
        'success': True,
        "questions": results
    }), 200


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
    Getting the questions by filtering according to the fields
'''

@bluePrint.route("/getQuestions", methods=["GET"])
@isAuth(request)
def getQuestions(user):

    # Get the request and validate it
    requestData = request.get_json()
    validation = validateQuestionQuery(requestData)

    # Parameters
    page = int(request.args.get('page')) if request.args.get('page') is not None else 1

    if validation['success'] is False:
        return jsonify(validation)

    # Perform the filtering operation
    status, message, results = filterQuestionsByAttributes(requestData, page)

    # Return the response
    return jsonify({
        'success': status,
        "questions": results,
        "message": message
    }), 200
