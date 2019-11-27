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


MIN_THRESHOLD = 40  # Minimum threshold for similarity RATE


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

    # Threshold parameter
    threshold = int(request.args.get('threshold')) if request.args.get('threshold') is not None else MIN_THRESHOLD

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

        questionsData = list(map(lambda x: {"questionId": x['question']['_id'], "similarityRate": x['similarity_rate']}, foundQuestions))

        searchedQuestion.setCacheData(questionsData)
        searchedQuestion.insert_one()

    # Result questions
    questions = searchedQuestion.get()

    # Filtering
    if threshold:
        questions = list(filter(lambda x: x['similarityRate'] > threshold, questions))

    # Response
    return jsonify({
        'success': True,
        "results": questions
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

    if validation['success'] is False:
        return jsonify(validation)

    # Perform the filtering operation
    results = filterQuestionsByAttributes(requestData)

    # Return the response
    return jsonify({
        'success': True,
        "results": results
    }), 200
