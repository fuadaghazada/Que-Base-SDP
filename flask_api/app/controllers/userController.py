from copy import deepcopy
from bson.objectid import ObjectId

from flask import Blueprint
from flask import jsonify
from flask import request

from app.models import User
from app.helpers.isAuth import isAuth

# Blue print
bluePrint = Blueprint('users', __name__, url_prefix='/users')


@bluePrint.route("/getUser", methods=["GET"])
@isAuth(request)
def getUser(user):

    # ID as parameter
    userId = request.args.get('id')

    result = None
    try:
        result = User({"_id": userId}).data()
    except Exception as e:
        print("NO SUCH USER ID")

    status = result is not None

    # Return the response
    return jsonify({
        'success': status,
        "user": result
    })


@bluePrint.route("/addFriend", methods=["POST"])
@isAuth(request)
def sendFriendRequest(user):

    currentUser = User({"_id": user["_id"]})
    otherUserId = request.args.get('id')

    status, message = False, "Something went wrong"

    friendModel = User({"_id": otherUserId})
    friendUser = friendModel.data()

    curWaitlist = currentUser.data().get('friendsWaitList')
    curWaitlist = list(curWaitlist) if curWaitlist else []

    otherWaitlist = friendUser.get('friendsWaitList')
    otherWaitlist = list(otherWaitlist) if otherWaitlist else []

    currentUserId = currentUser.data().get("_id")

    if currentUserId and str(currentUserId) != otherUserId:
        if currentUserId not in otherWaitlist and ObjectId(otherUserId) not in curWaitlist:
            otherWaitlist.append(currentUserId)
            status = True
            message = "Friend request is sent successfully"
        else:
            status = False
            message = "Request has been already sent"

    if status:
        setattr(friendModel, 'friendsWaitList', otherWaitlist)
        friendModel.update_one(vars(friendModel))

    # Response
    return jsonify({
        "success": status,
        "message": message
    }), 200


@bluePrint.route("/acceptFriend", methods=["POST"])
@isAuth(request)
def acceptFriendRequest(user):

    currentUserId = ObjectId(user["_id"])
    otherUserId = request.args.get('id')

    status, message = False, "Something went wrong"

    if currentUserId and str(currentUserId) != otherUserId:
        # User models
        currentUserModel = User({"_id": currentUserId})
        friendUserModel = User({"_id": otherUserId})

        currentUser = currentUserModel.data()
        friendUser = friendUserModel.data()

        curWaitlist = currentUser.get('friendsWaitList')
        curWaitlist = list(curWaitlist) if curWaitlist else []

        otherUserId = ObjectId(otherUserId)

        if otherUserId in curWaitlist:
            currentUserFriends = currentUser.get('friends')
            currentUserFriends = list(
                currentUserFriends) if currentUserFriends else []

            otherUserFriends = friendUser.get('friends')
            otherUserFriends = list(
                otherUserFriends) if otherUserFriends else []

            if otherUserId not in currentUserFriends:
                curWaitlist.remove(otherUserId)
                currentUserFriends.append(otherUserId)
                setattr(currentUserModel, 'friendsWaitList', curWaitlist)
                setattr(currentUserModel, 'friends', currentUserFriends)
                currentUserModel.update_one(vars(currentUserModel))

                if currentUserId not in otherUserFriends:
                    otherUserFriends.append(currentUserId)
                    setattr(friendUserModel, 'friends', otherUserFriends)
                    friendUserModel.update_one(vars(friendUserModel))

                    status = True
                    message = "Friend request is accepted"

    # Response
    return jsonify({
        "success": status,
        "message": message
    }), 200
