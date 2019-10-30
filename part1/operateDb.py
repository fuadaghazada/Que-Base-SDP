from copy import deepcopy

from connectDb import getDb
from analyze import analyzeQuestion

from pprint import pprint

'''
    Inserting the question to the DB

    :param (dict) questionObj: question dictinoary with the proper fields
    :param (bool) analyze: to determine if the question needs to be analyzed
'''
def insertQuestion(questionObj, analyze = False):

    # Type checking
    if type(questionObj) is not dict:
        raise TypeError("Please insert the question in 'dict' type")

    # Checking the body of question
    if "body" not in questionObj:
        raise ValueError("Question dictionary missed 'body' key")

    questionBody = questionObj["body"]

    # Question to be inserted
    question = deepcopy(questionObj)

    # Analyze part (Text Razor)
    if analyze is True:
        # Getting keywords from Text Razor
        entity_tags, topics, categories = analyzeQuestion(questionBody)

        # Adding the analyzed components as properties
        question["entity_tags"] = entity_tags
        question["topics"] = topics
        question["categories"] = categories

    # Inserting the question to the DB
    questionCollection = getDb()["questions"]
    questionCollection.insert_one(question)


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

        # DB collection
        questionCollection = getDb()["questions"]

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
        questionsFromSimilarTopic = questionCollection.find(query)

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

        for question in foundQuestions:
            print(f"{question['question']['body']} --- {question['similarity_rate']}% \n\n")

        # # Search query
        # query = {"$or": []}
        #
        # # Generating the query (entity_tags)
        # for entity_tag in entity_tags:
        #     query["$or"].append({"entity_tags": {
        #         "$elemMatch": {
        #             "label": entity_tag["label"]
        #         }
        #     }})
        #
        # # Results after checking entity_tag similarity
        # questionsFromSimilarEntityTags = questionCollection.find(query)
        # questionsFromSimilarEntityTagsIds = set([q['_id'] for q in questionsFromSimilarEntityTags])
        #
        # # Intersection results
        # common = questionsFromSimilarEntityTagsIds.intersection(questionsFromSimilarTopicIds)
        #
        # # TEMP - Getting the questons from the common ids
        # query = {"_id": {"$in": list(common)}}
        # questions = questionCollection.find(query)
        # for q in questions:
        #     print(q['body'], "\n")
        #
        # return common
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


'''
    Removal of non-analyzed documents
'''
def removeOnesWithoutAttrs():

    # DB collection
    questionCollection = getDb()["questions"]

    query = { "$and": [{"topics": None}, {"entity_tags": None}, {"categories": None}] }
    x = questionCollection.delete_many(query)


removeOnesWithoutAttrs()
