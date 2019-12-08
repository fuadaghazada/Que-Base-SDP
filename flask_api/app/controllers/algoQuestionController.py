import fasttext as ft

from bson.objectid import ObjectId

from flask import Blueprint
from flask import jsonify
from flask import request

from app.models import Question, User
from app.schemas import validateQuestion, validateFilterQuery
from app.helpers.isAuth import isAuth
from app.helpers.types import QuestionType
from app.helpers.query import CustomQueryGenerator
from app.helpers.constant import ALGO_MODEL_PATH
from app.helpers.filter import createFilterQuery

# Blue print
bluePrint = Blueprint('algoQuestions', __name__, url_prefix='/algoQuestions')


'''
    [POST] Retrieving similar questions with request
'''

@bluePrint.route("/findSimilarQuestions", methods=["POST"])
@isAuth(request)
def getSimilarQuestions(user):

    requestData = request.get_json()
    validation = validateQuestion(requestData)

    # Invalid
    if validation['success'] is False:
        return jsonify(validation)

    # -- Parameters --
    # Page
    page = int(request.args.get('page')) if request.args.get('page') is not None else 1

    # Extracting question body from the request
    questionBody = requestData.get("body")

    # Loading the model and predicting + some processing
    model = ft.load_model(ALGO_MODEL_PATH)
    result = model.predict(questionBody)
    label, reliabilty = result
    label = label[0] if len(label) > 0 else None
    label = label.replace('__label__', '').replace('-', ' ')

    # Generating the query
    query = CustomQueryGenerator()
    query.addLabelField(label)
    queryStatus, queryDict = query.getCompleteQuery()

    # Query check
    if not queryStatus:
        # Return response
        return jsonify({
            'success': False,
            'message': "Query is not valid"
        })

    # Filtering
    filtering = requestData.get("filter")
    sortingAttr, sortOrder = None, None
    if filtering:
        # Validating the filter Query data
        validation = validateFilterQuery(filtering)

        if validation['success'] is False:
            return jsonify(validation)

        # Filtering process
        filterData, message = createFilterQuery(filtering, QuestionType.ALGO)

        if not filterData:
            # Failed
            return jsonify({
                'success': False,
                "message": message
            })

        filterDict, sortingAttr, sortOrder = filterData
        queryDict = CustomQueryGenerator.appendTwoQueries(queryDict, filterDict)

    # Requesting the query
    results = Question.find(queryDict, sortingAttr = sortingAttr, sortOrder = sortOrder, pageNumber = page, type = QuestionType.ALGO)

    # Return response
    return jsonify({
        'success': True,
        'results': results
    })
