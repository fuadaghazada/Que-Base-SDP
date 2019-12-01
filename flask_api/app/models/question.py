import math
from copy import deepcopy

from app.utils.db import getDb
from app.utils.titleGeneration import generateTitleFromText
from app.helpers.analyze import analyzeQuestion
from app.helpers.constant import LIMIT

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
        self.title = question['title'] if question.get('title') else generateTitleFromText(self.body)
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
        :param: pageNumber - page number for pagination
    '''
    @staticmethod
    def find(query, sortingAttr = "_id", sortOrder = 1, pageNumber = 1):
        db = getDb()
        db[COLLECTION_NAME].create_index([("body", "text")])

        # Getting the question with the parameters: pagination and sort
        offset = (pageNumber - 1) * LIMIT
        cursor = db[COLLECTION_NAME].find(query)

        # TODO: try removing or update the try/except statement with better version
        # If sorting Attribute is not a valid one; do not sort
        try:
            if sortingAttr != "" or sortingAttr is not None:
                cursor = cursor.sort(sortingAttr, sortOrder)
        except Exception as e:
            pass

        count = cursor.count()
        results = cursor.skip(offset).limit(LIMIT)
        numberOfPages = math.ceil(count / LIMIT)

        return {
            "data": list(results),
            "numberOfPages": numberOfPages
        }


    '''
        Static method for returning the (one) result with the given query

        :param: query - the given query (Mongo)
    '''
    @staticmethod
    def find_one(query):
        db = getDb()

        result = db[COLLECTION_NAME].find_one(query)

        return result
