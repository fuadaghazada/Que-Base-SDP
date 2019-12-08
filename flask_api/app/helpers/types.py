from enum import Enum

ALGO_COLLECTION_NAME = "algQuestions"
SOC_COLLECTION_NAME = "questions"

'''
    Possible question types
'''
class QuestionType(Enum):
    SOC = 1
    ALGO = 2


'''
    Returning the collection name according to question type
'''
def getCollectionName(type = QuestionType.SOC):

    collectionName = SOC_COLLECTION_NAME

    if type == QuestionType.SOC:
        collectionName = SOC_COLLECTION_NAME
    elif type == QuestionType.ALGO:
        collectionName = ALGO_COLLECTION_NAME

    return collectionName
