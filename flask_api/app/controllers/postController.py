from bson.objectid import ObjectId

from flask import Blueprint
from flask import jsonify
from flask import request

from app.models import Post, User

from app.schemas import validatePost

from app.helpers.isAuth import isAuth


# Blue print
bluePrint = Blueprint('posts', __name__, url_prefix='/posts')

'''
    [GET] Getting a post according to its id
'''

@bluePrint.route("/getPost", methods=["GET"])
@isAuth(request)
def getPost(user):

    # ID as parameter
    postId = request.args.get('id')

    userId = user["_id"]
    user = User({"_id": userId})

    result = None
    try:
        post = Post({"_id": postId})
        result = post.data()
    except Exception as e:
        print("NO SUCH POST ID")
        raise e

    status = result is not None

    # Return the response
    return jsonify({
        'success': status,
        "post": result
    }), 200


@bluePrint.route("/getPosts", methods=["GET"])
@isAuth(request)
def getPosts(user):

    userId = user["_id"]
    user = User({"_id": userId}).data()
    userFeedList = user.get("feedList") if user.get("feedList") else []

    # Parameters
    page = int(request.args.get('page')) if request.args.get('page') is not None else 1

    results = []
    try:
        results = Post.find({"_id": {"$in": userFeedList}}, sortOrder = -1, sortingAttr = 'timestamp', pageNumber = page)

    except Exception as e:
        print("NO SUCH POST ID")
        raise e

    status = results != []

    # Return the response
    return jsonify({
        'success': status,
        "result": results
    }), 200
