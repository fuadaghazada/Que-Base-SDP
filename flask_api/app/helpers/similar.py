from copy import deepcopy

from numpy import dot
from numpy.linalg import norm

from app.models.question import Question
from app.helpers.analyze import analyzeQuestion

from bson.json_util import dumps


'''
    Searching a question after analyzing it

    :param (str) questionBody: text of the question itself
'''
def findSimilarQuestions(questionBody):

    try:
        # Analyzing the question
        entity_tags, topics, categories = analyzeQuestion(questionBody)

        # Search query
        query = {"$or": []}

        # Generating the query (topic)
        for topic in topics:
            query["$or"].append({"topics": {
                "$elemMatch": {
                    "label": {
                        "$regex": topic["label"],
                        "$options": "i"
                    }
                }
            }})

        # No topic is found
        if len(topics) == 0:
            return None

        # Results after checking topic similarity
        questionsFromSimilarTopic = Question.findGeneric(query)

        # Query returns None
        if not questionsFromSimilarTopic:
            return None

        # Score algorithm
        foundQuestions = []
        for question in questionsFromSimilarTopic:

            questionTopics = question['topics']

            currentVector, questionVector = createTwoVectorsFromTopics(topics, questionTopics)
            cosSimilarity = round(cosineSimilarity(currentVector, questionVector) * 100, 2)

            foundQuestions.append({'question': question, 'similarity_rate': cosSimilarity})

        # Sorting according to the topic score
        foundQuestions = sorted(foundQuestions, key = lambda x: x['similarity_rate'], reverse = True)

        for i in range(len(foundQuestions)):

            # We do not need them in the response (probably)
            del foundQuestions[i]['question']['entity_tags']
            del foundQuestions[i]['question']['topics']
            del foundQuestions[i]['question']['categories']

        return foundQuestions

    except Exception as e:
        raise e
        return []



'''
    Creating two vectors from the two topic list of dictionaries

    :param: (list) vector1 - first topic list
    :param: (list) vector2 - second topic list

    :return (tuple) vector1, vector2 - tuple of created vectors
'''
def createTwoVectorsFromTopics(topics1, topics2):

    # Creating topic dictionaries
    topics1Dict = {}
    for topic in topics1:
        topics1Dict[topic['label']] = topic['score']

    topics2Dict = {}
    for topic in topics2:
        topics2Dict[topic['label']] = topic['score']

    # Sperating topic labels & applying union & sorting
    labels1 = [topic['label'] for topic in topics1]
    labels2 = [topic['label'] for topic in topics2]

    all_labels = set(labels1).union(set(labels2))
    all_labels = sorted(list(all_labels), reverse=False)

    vector1, vector2 = [], []
    for label in all_labels:
        score1 = topics1Dict.get(label) if topics1Dict.get(label) else 0
        score2 = topics2Dict.get(label) if topics2Dict.get(label) else 0
        vector1.append(score1)
        vector2.append(score2)

    return vector1, vector2


'''
    Calculating the cosine similarity of two given vectors

    :param: (list) vector1 - first vector
    :param: (list) vector2 - second vector

    :return: (float) cosineSimilarity
'''
def cosineSimilarity(vector1, vector2):
    return dot(vector1, vector2) / (norm(vector1) * norm(vector2))


'''
    Given the topics calculates the maximum possible score
'''
def calculateMaxPossibleScore(topics):

    maxScore = 0.0
    for topic in topics:
        maxScore += topic['score'] ** 2

    return maxScore
