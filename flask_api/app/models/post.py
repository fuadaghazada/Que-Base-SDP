from bson.objectid import ObjectId
from datetime import datetime, timedelta

from app.models import Model, User
from app.utils.db import getDb

COLLECTION_NAME = "posts"

'''
    Model class for post
'''
class Post(Model):
    '''
        Initializing a post

        :param: (string) postObj - the post object with its properties
    '''
    def __init__(self, postObj):

        super().__init__(postObj, COLLECTION_NAME)

        if vars(self) == {}:
            self.userId = ObjectId(postObj["userId"])
            self.message = postObj["message"]
            self.timestamp = datetime.utcnow() + timedelta(hours = 3)
            self.questionId = ObjectId(postObj.get('questionId')) if postObj.get('questionId') else None
            self.questionTitle = postObj.get('questionTitle') if postObj.get('questionTitle') else None

    '''
        Inserting into db
    '''
    def insert_one(self):
        db = getDb()

        # Statuses for existence
        postExists = self.check_exists()

        if postExists is True:
            return False, "Post already exists"
        else:
            # Insertion
            result = db[COLLECTION_NAME].insert_one(vars(self))
            postId = ObjectId(result.inserted_id)

            user = User({"_id": self.userId}).data()
            userFriends = user['friends']

            for friendId in userFriends:
                friend = User({"_id": friendId})
                friend.addFeed(postId)

            return True, "Post is created successfully"


    '''
        Static method for returning the result (posts) with the given query

        :param: query - the given query (Mongo)
        :param: pageNumber - page number for pagination
    '''
    def find(query, sortingAttr = "_id", sortOrder = 1, pageNumber = 1):

        return Model.find(COLLECTION_NAME, query, sortingAttr, sortOrder, pageNumber)


    '''
        Determining whether a post with such message exists in DB

        :return: (bool) status for existence
    '''
    def check_exists(self):
        db = getDb()

        messageExisting = db[COLLECTION_NAME].find_one({"message": self.message, "questionId": self.questionId})
        messageResult = True if messageExisting is not None else False

        return messageResult
