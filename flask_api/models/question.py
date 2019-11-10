from db import getDb
from helpers.analyze import analyzeQuestion

COLLECTION_NAME = "questions"

'''
    Model class for question
'''
class Question():
    '''
        Initializing a question

        :param: (string) body - text body of the question
    '''
    def __init__(self, body):
        self.body = body


    '''
        Inserting a question with its analysis to DB

        :param: (bool) analyze - flag for determining the analysis
        :return: (tuple) (status, message)
    '''
    def insert_one(self, analyze = True):
        db = getDb()

        # Check if the same question exists
        if self.check_exists():
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
