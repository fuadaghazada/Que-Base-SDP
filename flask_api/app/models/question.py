from copy import deepcopy

from app.utils.db import getDb
from app.helpers.analyze import analyzeQuestion

COLLECTION_NAME = "questions"

'''
    Model class for question
'''
class Question():
    '''
        Initializing a question

        :param: (string) question - the question with its properties
    '''
    def __init__(self, question):
        self.body = question['body']
        self.source = question['source'] if question.get('source') else None
        self.userId = question['userId'] if question.get('userId') else None
        self.viewCount = question['viewCount'] if question.get('viewCount') else 0
        self.favCount = question['favCount'] if question.get('favCount') else 0


    '''
        Inserting a question with its analysis to DB

        :param: (bool) analyze - flag for determining the analysis
        :return: (tuple) (status, message)
    '''
    def insert_one(self, analyze = True):
        db = getDb()

        # Check if the same question exists
        if self.check_exists():

            obj = deepcopy(vars(self))
            del obj['body']
            newValues = {"$set": obj}

            x = db[COLLECTION_NAME].update_one({"body": self.body}, newValues)
            print(x.raw_result)

            return False, "Question already exists"
        else:
            # Analyze
            if analyze is True:
                entity_tags, topics, categories = analyzeQuestion(self.body)

                self.entity_tags = entity_tags
                self.topics = topics
                self.categories = categories

            # Insertion
            db[COLLECTION_NAME].insert_one(vars(self))

        return True, "Question is inserted"


    '''
        Determining whether a same question with exactly the same body check_exists in DB

        :return: (bool) status
    '''
    def check_exists(self):
        db = getDb()

        existing = db[COLLECTION_NAME].find_one({"body": self.body})

        if existing is not None:
            return True

        return False


    '''
        Static method for returning the result with the given query

        :param: query - the given query (Mongo)
    '''
    @staticmethod
    def find(query):
        db = getDb()
        return db[COLLECTION_NAME].find(query)
