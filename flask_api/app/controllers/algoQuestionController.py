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
    questionBody = requestData['body']

    # Loading the model and predicting + some processing
    model = ft.load_model(ALGO_MODEL_PATH)
    result = model.predict(questionBody)
    label, reliabilty = result
    label = label[0] if len(label) > 0 else None
    labels = label.replace('__label__', '').split(',')

    # Return response
    return jsonify({
        'success': True,
        'result': labels
    })
