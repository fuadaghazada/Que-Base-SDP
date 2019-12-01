from bson.objectid import ObjectId

from flask import Blueprint
from flask import jsonify
from flask import request

from app.models import Question, SearchedQuestion, User

from app.schemas import validateQuestion, validateFilterQuery

from app.helpers.similar import findSimilarQuestions
from app.helpers.isAuth import isAuth
from app.helpers.filter import createFilterQuery
from app.helpers.constant import MIN_THRESHOLD


# Blue print
bluePrint = Blueprint('questions', __name__, url_prefix='/questions')

'''
    [POST] Retrieving similar questions with request
'''

@bluePrint.route("/findSimilarQuestions", methods=["POST"])
@isAuth(request)
def getSimilarQuestions(user):

    requestData = request.get_json()
    validation = validateQuestion(requestData)

    # -- Parameters --
    # Threshold
    threshold = int(request.args.get('threshold')) if request.args.get('threshold') is not None else MIN_THRESHOLD
    threshold = MIN_THRESHOLD if threshold < MIN_THRESHOLD else threshold

    # Page
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

    # Filtering
    filterData = None
    filtering = requestData.get("filter")
    if filtering:
        # Validating the filter Query data
        validation = validateFilterQuery(filtering)

        if validation['success'] is False:
            return jsonify(validation)

        # Filtering process
        filterData, message = createFilterQuery(filtering)

    # Result questions
    results = searchedQuestion.get(threshold, pageNumber=page, filterData=filterData)
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
    [GET] Getting a question according to its id
'''

@bluePrint.route("/getQuestion", methods=["GET"])
@isAuth(request)
def getQuestion(user):

    # ID as parameter
    id = request.args.get('id')

    result = None
    try:
        result = Question({"_id": id}).data()
    except Exception as e:
        print("NO SUCH QUESTION ID")

    status = result is not None

    # Return the response
    return jsonify({
        'success': status,
        "question": result
    }), 200
