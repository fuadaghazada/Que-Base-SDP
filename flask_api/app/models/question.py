from copy import deepcopy

from app.models import Model
from app.utils.db import getDb
from app.utils.titleGeneration import generateTitleFromText
from app.helpers.types import QuestionType
from app.helpers.analyze import analyzeQuestion
from app.helpers.types import getCollectionName


'''
    Model class for question
'''
class Question(Model):
    '''
        Initializing a question

        :param: (string) question - the question with its properties
    '''
    def __init__(self, question, type = QuestionType.SOC):

        # Determining the collection name first
        collectionName = getCollectionName(type)

        super().__init__(question, collectionName)

        if vars(self) == {}:
            self.body = question['body']
            self.title = question['title'] if question.get('title') else generateTitleFromText(self.body)
            self.source = question['source'] if question.get('source') else None
            self.userId = question['userId'] if question.get('userId') else None
            self.viewCount = question['viewCount'] if question.get('viewCount') else 0
            self.favCount = question['favCount'] if question.get('favCount') else 0

            if type == QuestionType.ALGO:
                self.labels = question['labels'] if question.get('labels') else []
                self.level = question['level'] if question.get('level') else None

            self.type = type
            self.collectionName = collectionName


    '''
        Inserting a question with its analysis to DB

        :param: (bool) analyze - flag for determining the analysis
        :return: (tuple) (status, message)
    '''
    def insert_one(self, analyze = True):
        db = getDb()

        # Check if the same question exists
        if self.check_exists():
            return False, "Question already exists", None
        else:
            # Analyze
            if analyze is True and self.type == QuestionType.SOC:
                entity_tags, topics, categories = analyzeQuestion(self.body)

                self.entity_tags = entity_tags
                self.topics = topics
                self.categories = categories

            # Insertion
            result = db[self.collectionName].insert_one(self.data())
            questionId = result.inserted_id

        return True, "Question is inserted", questionId


    '''
        Updating the question properties

        :param: updateValues - new values for update
    '''
    def update_one(self, updateValues):
        super().update_one(updateValues, "questions")   # TODO: Hard coded


    '''
        Determining whether a same question with exactly the same body check_exists in DB

        :return: (bool) status
    '''
    def check_exists(self):
        db = getDb()

        existing = db[self.collectionName].find_one({"body": self.body})

        if existing is not None:
            return True

        return False


    '''
        Static method for returning the result (questions) with the given query

        :param: query - the given query (Mongo)
        :param: pageNumber - page number for pagination
    '''
    @staticmethod
    def find(query, sortingAttr = "_id", sortOrder = 1, pageNumber = 1, type = QuestionType.SOC):
        db = getDb()
        collectionName = getCollectionName(type)
        db[collectionName].create_index([("body", "text")])

        return Model.find(collectionName, query, sortingAttr, sortOrder, pageNumber)


    '''
        Getting the model data: question data (by deleting unnecessary attributes)
    '''
    def data(self):

        try:
            delattr(self, 'type')
        except AttributeError as e:
            print("No such attribute")

        return super().data()


    def incrementViewCount(self):

        self.viewCount = self.viewCount + 1
        self.update_one(vars(self))


    def updateFavCount(self, increment=True):

        if increment:
            self.favCount = self.favCount + 1
        else:
            self.favCount = self.favCount - 1
        self.update_one(vars(self))
