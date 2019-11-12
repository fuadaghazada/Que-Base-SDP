from app.utils.db import getDb
from app.utils.encrypt import hashPassword, validatePassword

COLLECTION_NAME = "users"


'''
    Model class for user
'''
class User():
    '''
        Creating a user

        :param: (dict) userObj - object contains the properties of the user
    '''
    def __init__(self, userObj):
        self.firstname = userObj["firstname"]
        self.lastname = userObj["lastname"]
        self.username = userObj["username"]
        self.email = userObj["email"]
        self.password = hashPassword(userObj["password"])         # TODO: Hash the password


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
