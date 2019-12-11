from bson.objectid import ObjectId

from flask import Blueprint
from flask import jsonify
from flask import request

from app.models import Question, User

from app.schemas import validateQuestion, validateFilterQuery

from app.helpers.isAuth import isAuth
from app.helpers.filter import createFilterQuery


# Blue print
bluePrint = Blueprint('questions', __name__, url_prefix='/questions')


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
    [POST] Favorite/disfavorite a question given its id
'''

@bluePrint.route("/favoriteQuestion", methods=["POST"])
@isAuth(request)
def favoriteQuestion(user):

    # Question ID as parameter & userID from header
    questionId = request.args.get('id')
    userId = user["_id"]

    # Converting str into Object ID
    questionId = ObjectId(questionId)

    # Getting the user adding the favorite questions to list
    user = User({"_id": userId})

    status, message = False, ""

    curFavoriteQuestions = user.data().get('favoriteQuestions')
    curFavoriteQuestions  = list(curFavoriteQuestions) if curFavoriteQuestions else []

    if questionId not in curFavoriteQuestions:
        curFavoriteQuestions.append(questionId)
        status = True
        message = "Questions is added to the favorite list!"
    else:
        curFavoriteQuestions.remove(questionId)
        status = False
        message = "Questions is removed from the favorite list!"

    setattr(user, 'favoriteQuestions', curFavoriteQuestions)

    # Updating
    user.update_one(user.data())

    # Return the response
    return jsonify({
        'success': True,
        'result': status,
        'message': message
    }), 200


'''
    [GET] Getting if the question is in the favorite list of the logged user
'''

@bluePrint.route("/isFavorite", methods=["GET"])
@isAuth(request)
def isFavoriteQuestion(user):

    result = False

    # ID as parameter
    questionId = request.args.get('id')

    userId = user["_id"]
    user = User({"_id": userId})

    # Favorite questions of the user
    favoriteQuestions = user.data().get('favoriteQuestions')
    result = ObjectId(questionId) in favoriteQuestions

    # Response
    return jsonify({
        'success': True,
        'result': result
    })

'''
    [GET] Getting a question according to its id
'''

@bluePrint.route("/getQuestion", methods=["GET"])
@isAuth(request)
def getQuestion(user):

    # ID as parameter
    questionId = request.args.get('id')

    userId = user["_id"]
    user = User({"_id": userId})

    result = None
    try:
        result = Question({"_id": questionId}).data()
    except Exception as e:
        print("NO SUCH QUESTION ID")
        raise e

    # Favorite questions of the user
    favoriteQuestions = user.data().get('favoriteQuestions')
    isFavorite = ObjectId(questionId) in favoriteQuestions

    status = result is not None

    # Return the response
    return jsonify({
        'success': status,
        "question": result,
        "favorite": isFavorite
    }), 200


@bluePrint.route("/userQuestions", methods=["GET"])
@isAuth(request)
def getUserQuestions(user):

    status, message = False, "Something went wrong"

    # Parameters
    uploaderId = request.args.get('id')  # id of the user whose questions are to be shown
    page = int(request.args.get('page')) if request.args.get('page') is not None else 1

    # Get the id of the current user
    currentUserId = ObjectId(user["_id"])

    # Get the current user model
    currentUserModel = User({"_id": currentUserId})
    currentUser = currentUserModel.data()

    # Get the friend list of the current user
    currentUserFriends = currentUser.get('friends')
    currentUserFriends = list(currentUserFriends) if currentUserFriends else []

    results = []

    # Ensure that the other user (uploader) is a friend of ours
    if ObjectId(uploaderId) in currentUserFriends or str(currentUserId) == uploaderId:

        # Get the questions
        results = Question.find({"userId": uploaderId}, pageNumber = page)
        status, message = True, "Questions are retrieved successfully"

    else:
        status, message = False, "To be able to view the questions uploaded by that user, you must be friends"

    # Response
    return jsonify({
        "success": status,
        "message": message,
        "result": results
    }), 200


@bluePrint.route("/mostViewed", methods=["GET"])
@isAuth(request)
def getMostViewedQuestions(user):

    # Parameters
    page = int(request.args.get('page')) if request.args.get('page') is not None else 1
    threshold = int(request.args.get('threshold')) if request.args.get('threshold') is not None else 0

    sortingAttr = 'viewCount'
    sortOrder = -1
    results = Question.find({"viewCount": {"$gt": threshold}}, sortingAttr, sortOrder, page)

    # Response
    return jsonify({
        "success": True,
        "result": results
    }), 200
