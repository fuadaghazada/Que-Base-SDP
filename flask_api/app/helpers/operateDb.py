from copy import deepcopy

from app.models.question import Question
from app.helpers.analyze import analyzeQuestion


'''
    Searching a question after analyzing it

    :param (str) questionBody: text of the question itself
'''
def findSimilarQuestions(questionBody):

    try:
        # Analyzing the question
        entity_tags, topics, categories = analyzeQuestion(questionBody)
        maxTopicScore = calculateMaxPossibleScore(topics)

        # Creating dict from input question topics
        topicsDict = {}
        for topic in topics:
            topicsDict[topic['label']] = topic['score']

        # Search query
        query = {"$or": []}

        # Generating the query (topic)
        for topic in topics:
            query["$or"].append({"topics": {
                "$elemMatch": {
                    "label": topic["label"],
                    "score": {"$gte": 0}
                }
            }})

        # Results after checking topic similarity
        questionsFromSimilarTopic = Question.find(query)

        # Score algorithm
        foundQuestions = []
        for question in questionsFromSimilarTopic:
            topicScore = 0.0
            for topic in question['topics']:
                if topicsDict.get(topic['label']) is not None:
                    topicScore += topic['score'] * topicsDict[topic['label']]

            foundQuestions.append({'question': question, 'score': topicScore})

        # Sorting according to the topic score
        foundQuestions = sorted(foundQuestions, key = lambda x: x['score'], reverse = True)

        for i in range(len(foundQuestions)):
            foundQuestions[i]['similarity_rate'] = round((foundQuestions[i]['score'] / maxTopicScore) * 100, 2)

            # We do not need them in the response (probably)
            del foundQuestions[i]['question']['entity_tags']
            del foundQuestions[i]['question']['topics']
            del foundQuestions[i]['question']['categories']


        for question in foundQuestions:
            print(f"{question['question']['body']} --- {question['similarity_rate']}% \n\n")

        return foundQuestions

    except Exception as e:
        raise e
        return []


'''
    Given the topics calculates the maximum possible score
'''
def calculateMaxPossibleScore(topics):

    maxScore = 0.0
    for topic in topics:
        maxScore += topic['score'] ** 2

    return maxScore