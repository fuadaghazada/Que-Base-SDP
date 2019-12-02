from copy import deepcopy
from bson.objectid import ObjectId

from app.models import Model
from app.utils.db import getDb
from app.utils.encrypt import hashPassword, validatePassword

COLLECTION_NAME = "users"


'''
    Model class for user
'''
class User(Model):
    '''
        Creating a user

        :param: (dict) userObj - object contains the properties of the user
    '''
    def __init__(self, userObj):

        super().__init__(userObj, COLLECTION_NAME)

        if vars(self) == {}:
            self.firstname = userObj["firstname"]
            self.lastname = userObj["lastname"]
            self.username = userObj["username"]
            self.email = userObj["email"]
            self.password = hashPassword(userObj["password"])
            self.favoriteQuestions = []
            self.friends = []


    '''
        Inserting into db (Registering)
    '''
    def insert_one(self):
        db = getDb()

        # Statuses for existence
        usernameExists, emailExists = self.check_exists()

        if usernameExists is True:
            return False, "Username already exists"
        elif emailExists is True:
            return False, "Email already exists"
        else:
            # Insertion
            db[COLLECTION_NAME].insert_one(vars(self))

            return True, "User is created successfully"

    '''
        Updating the question properties

        :param: updateValues - new values for update
    '''
    def update_one(self, updateValues):
        super().update_one(updateValues, COLLECTION_NAME)


    '''
        Getting the user
    '''
    @staticmethod
    def find_one(email, password):
        db = getDb()

        # Fetching...
        user = db[COLLECTION_NAME].find_one({"email": email})

        # If no user
        if user is None:
            return None

        userPassword = user['password']

        # Password validation
        isCorrectPassword = validatePassword(userPassword, password)

        if isCorrectPassword is True:
            userData = deepcopy(user)
            del userData['password']     # Removing the password

            return userData
        else:
            return None


    '''
        Determining whether a user with such username/email exists in DB

        :return: (bool, bool) statuses for username and email
    '''
    def check_exists(self):
        db = getDb()

        usernameExisting = db[COLLECTION_NAME].find_one({"username": self.username})
        emailExisting = db[COLLECTION_NAME].find_one({"email": self.email})

        usernameResult = True if usernameExisting is not None else False
        emailResult = True if emailExisting is not None else False

        return usernameResult, emailResult


    '''
        Static method for returning the result (users) with the given query

        :param: query - the given query (Mongo)
        :param: pageNumber - page number for pagination
    '''
    def find(query, sortingAttr = "_id", sortOrder = 1, pageNumber = 1):

        return Model.find(COLLECTION_NAME, query, sortingAttr, sortOrder, pageNumber)


    '''
        Adding/Removing the question to favorite questions

        :param: questionId - the id of the question to be added
    '''
    def favoriteQuestion(self, questionId):

        status, message = False, ""

        curFavoriteQuestions = vars(self).get('favoriteQuestions')
        curFavoriteQuestions  = list(curFavoriteQuestions) if curFavoriteQuestions else []

        if questionId not in curFavoriteQuestions:
            curFavoriteQuestions.append(questionId)
            status = True
            message = "Questions is added to the favorite list!"
        else:
            curFavoriteQuestions.remove(questionId)
            status = False
            message = "Questions is removed from the favorite list!"

        setattr(self, 'favoriteQuestions', curFavoriteQuestions)

        # Updating
        self.update_one(vars(self))

        return status, message
