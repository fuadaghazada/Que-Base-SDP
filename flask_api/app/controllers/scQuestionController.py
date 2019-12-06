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
bluePrint = Blueprint('scQuestions', __name__, url_prefix='/scQuestions')

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
