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


@bluePrint.route("/searchUser", methods=["GET"])
@isAuth(request)
def searchUsers(user):

    # Current user data
    currentUser = User({"_id": user["_id"]}).data()
    currentUserId = currentUser.get("_id")
    currentUserWaitlist = currentUser.get("friendsWaitList") if currentUser.get("friendsWaitList") else []
    currentUserFriends = currentUser.get("friends") if currentUser.get("friends") else []

    # Parameters
    page = int(request.args.get('page')) if request.args.get('page') is not None else 1
    searchUsername = request.args.get('username')

    results = User.find({"$and": [{"username": {"$regex": f"^{searchUsername}", "$options": "i"}}, {"username": {"$ne": currentUser["username"]}}]}, pageNumber = page)

    # All condititons
    resultUsers = []
    for searchUser in results["data"]:

        # Search user data
        searchUserId = searchUser.get("_id")
        searchUsername = searchUser.get("username")
        searchUserWaitlist = searchUser.get("friendsWaitList") if searchUser.get("friendsWaitList") else []
        searchUserFriends = searchUser.get("friends") if searchUser.get("friends") else []

        """
            CASE 1: Search user is in our friend list
            CASE 2: Search user has sent friend request to us (in our waitlist)
            CASE 3: We have sent him/her friend requets (we are in his/her waitlist)
            CASE 4: We are not related

            Note: userState will be related to case numbers
        """

        userState = 4
        message = f"You have no connection with {searchUsername}"
        resultUser = {"data": searchUser}

        if searchUserId in currentUserFriends:
            userState = 1
            message = f"You are friends with {searchUsername}"
        elif searchUserId in currentUserWaitlist:
            userState = 2
            message = f"{searchUsername} has sent friend request to you"
        elif currentUserId in searchUserWaitlist:
            userState = 3
            message = f"You have sent friend request to {searchUsername}"

        resultUser["state"] = userState
        resultUser["message"] = message
        resultUsers.append(resultUser)

    # Response
    return jsonify({
        "success": True,
        "results": resultUsers
    })


@bluePrint.route("/updateUser", methods=["POST"])
@isAuth(request)
def updateUser(user):

    requestData = request.get_json()
    currentUser = User({"_id": user["_id"]})
    status, message = False, "Something went wrong"

    if currentUser.update_one(requestData):
        status, message = True, "Update successful"
    # Response
    return jsonify({
        "success": status,
        "message": message
    }), 200

@bluePrint.route("/friends", methods=["GET"])
@isAuth(request)
def getFriends(user):

    status, message = False, "Something went wrong"

    # Get the id of the current user
    currentUserId = ObjectId(user["_id"])

    # Parameters
    otherUserId = request.args.get('id')  # id of the user whose friends are to be viewed
    page = int(request.args.get('page')) if request.args.get('page') is not None else 1

    # Get the corresponding user models
    currentUserModel = User({"_id": currentUserId})
    currentUser = currentUserModel.data()
    otherUserModel = User({"_id": otherUserId})
    otherUser = otherUserModel.data()

    # Get the friend list of the current user
    currentUserFriends = currentUser.get('friends')
    currentUserFriends = list(currentUserFriends) if currentUserFriends else []

    results = []

    # To be able to view the friends of the other user, the current user and the other one must be friends
    if ObjectId(otherUserId) in currentUserFriends or str(currentUserId) == otherUserId:

        # Get the friend list of the other user (only their id's)
        friendsIds = otherUser['friends']
        results = User.find({"_id": {"$in": friendsIds}}, pageNumber = page)

        status = True
        message = "Friend list is returned succesfully"

    # Otherwise, friends of the other user are not visible to our current user
    else:
        status = False
        message = "To be able to view the friends of that user, you must be friends"

    # Response
    return jsonify({
        "success": status,
        "message": message,
        "result": results
    }), 200


@bluePrint.route("/waitlist", methods=["GET"])
@isAuth(request)
def getWaitList(user):

    status, message = False, "Something went wrong"

    # Get the id of the current user
    currentUserId = ObjectId(user["_id"])

    # Parameters
    receivedId = request.args.get('id')  # id of the user whose wait list (friend requests) are to be viewed
    page = int(request.args.get('page')) if request.args.get('page') is not None else 1

    results = []

    # A user can only view his/her own wait list (friend requests)
    if str(currentUserId) == receivedId:

        # Get the user model
        currentUserModel = User({"_id": currentUserId})
        currentUser = currentUserModel.data()

        # Get the wait list
        curWaitlist = currentUser.get('friendsWaitList')
        curWaitlist = list(curWaitlist) if curWaitlist else []
        results = User.find({"_id": {"$in": curWaitlist}}, pageNumber = page)

        status = True
        message = "Wait list (friend requests) are retrieved successfully"

    else:
        status = False
        message = "You cannot view the wait list (friend requests) of that user"

    # Response
    return jsonify({
        "success": status,
        "message": message,
        "result": results
    }), 200