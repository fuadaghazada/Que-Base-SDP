from copy import deepcopy
from datetime import datetime

from .question import COLLECTION_NAME as QUESTIONS
from app.utils.db import getDb


COLLECTION_NAME = "searchedQuestions"
EXPIRE_TIME = 120

'''
    Model class for cache for searching
'''
class SearchedQuestion():

    '''
        Initializing a searched question

        :param: (string) data - the question with its properties
    '''
    def __init__(self, data):
        self.body = data['body']


    '''
        Inserting a question with its analysis to DB

        :return: (tuple) (status, message)
    '''
    def insert_one(self):
        db = getDb()

        # Temporay document indexing
        db[COLLECTION_NAME].create_index([('createdAt', 1), ("expireAfterSeconds", EXPIRE_TIME)])

        if self.check_exists():
            return False, "This question has already been searched"
        else:
            insertData = deepcopy(vars(self))
            insertData['createdAt'] = datetime.now()

            db[COLLECTION_NAME].insert_one(insertData)

        return True, "Question is inserted into searched collection"


    '''
        Determining whether a questions is searched before

        :return: (bool) status
    '''
    def check_exists(self):
        db = getDb()

        existing = db[COLLECTION_NAME].find_one({"body": self.body})

        if existing is not None:
            # Setting the existing data
            self.questionsData = existing['questionsData']

            return True

        return False


    '''
        Setting the cache data
    '''
    def setCacheData(self, questionsData):
        self.questionsData = questionsData


    '''
        Static method for returning the results with the given query
    '''
    def get(self):
        db = getDb()

        if self.questionsData:

            questionsIds = list(map(lambda x: x['questionId'], self.questionsData))
            similarityRates = list(map(lambda x: x['similarityRate'], self.questionsData))

            questions = list(db[QUESTIONS].find({"_id": {"$in": questionsIds}}))
            questions.sort(key = lambda question: questionsIds.index(question['_id']))

            # Adding the similarity rates to the result
            for i in range(len(questions)):
                questions[i]['similarityRate'] = similarityRates[i]

            return questions

        else:
            return None
