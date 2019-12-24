from bson.objectid import ObjectId

from flask import Blueprint
from flask import jsonify
from flask import request

from app.models import Question, User, Post

from app.schemas import validateQuestion, validateFilterQuery, validatePost

from app.helpers.isAuth import isAuth
from app.helpers.filter import createFilterQuery
from app.helpers.types import QuestionType

from app.utils.youtubeSearch import searchByKey


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

    # Parameters
    type = int(request.args.get('type')) if request.args.get('type') else 0
    type = QuestionType.SOC if type == 0 else QuestionType.ALGO

    # Invalid
    if validation['success'] is False:
        return jsonify(validation)

    try:
        # Inserting
        requestData['userId'] = user["_id"]
        userData = User({"_id": ObjectId(user['_id'])}).data()
        status, msg, questionId = Question(requestData, type = type).insert_one()

        # Response obj
        response = {
            "success": status,
            "message": msg
        }

        # Checking the status of insertion
        if status is True:
            response["question"] = requestData

        username = userData['username']
        message = f"{username} uploaded a question"

        # Creating & inserting a post
        postObj = {
            "userId": str(user["_id"]),
            "message": message,
            "questionId": str(questionId)
        }
        validation = validatePost(postObj)

        # Invalid
        if validation['success'] is False:
            return jsonify(validation)

        post = Post(postObj)
        post.insert_one()

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
    username = user.data()['username']

    status, message = False, ""

    curFavoriteQuestions = user.data().get('favoriteQuestions')
    curFavoriteQuestions  = list(curFavoriteQuestions) if curFavoriteQuestions else []

    question = Question({"_id": questionId})
    if questionId not in curFavoriteQuestions:
        question.updateFavCount()
        curFavoriteQuestions.append(questionId)
        status = True
        message = f"{username} favorited a question"

        # Creating & inserting a post
        postObj = {
            "userId": userId,
            "message": message,
            "questionId": str(questionId)
        }
        validation = validatePost(postObj)

        # Invalid
        if validation['success'] is False:
            return jsonify(validation)

        post = Post(postObj)
        post.insert_one()

    else:
        question.updateFavCount(False)
        curFavoriteQuestions.remove(questionId)
        status = False
        message = f"{username} unfavorited a question"

    setattr(user, 'favoriteQuestions', curFavoriteQuestions)

    # Updating
    user.update_one(user.data())

    # Return the response
    return jsonify({
        'success': True,
        'result': status,
        'message': message,
        'question': question.data()
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
        question = Question({"_id": questionId})
        question.incrementViewCount()
        result = question.data()
    except Exception as e:
        print("NO SUCH QUESTION ID")
        raise e

    # Favorite questions of the user
    favoriteQuestions = user.data().get('favoriteQuestions')
    isFavorite = ObjectId(questionId) in favoriteQuestions

    # YouTube search
    if result and result.get('labels'):
        youtubeResults = []
        try:
            searchKey = f"{result['title']} {result['source']['reference']} solution"
            youtubeResults = searchByKey(searchKey, 5)
            youtubeVideos = youtubeResults.get('videos')
            youtubeVideos.reverse()
            result['youtubeVideos'] = youtubeVideos

        except Exception as e:
            print("NO YOUTUBE VIDEO IS FOUND")

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
