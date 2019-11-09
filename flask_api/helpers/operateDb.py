from copy import deepcopy

from helpers.analyze import analyzeQuestion


'''
    Inserting the question to the DB

    :param (dict) questionObj: question dictinoary with the proper fields
    :param (Object) db: database object for db connection
    :param (bool) analyze: to determine if the question needs to be analyzed
'''
def insertQuestion(questionObj, db, analyze = False):

    # Type checking
    if type(questionObj) is not dict:
        raise TypeError("Please insert the question in 'dict' type")

    # Checking the body of question
    if "body" not in questionObj:
        raise ValueError("Question dictionary missed 'body' key")

    # Collection of questions
    questionCollection = db["questions"]

    # Question properties
    questionBody = questionObj["body"]

    # Check if exists in db
    existingQuestion = questionCollection.find_one({"body": questionBody})

    if existingQuestion is not None:
        msg = "The question already exists in the DB"
        print(msg)
        return False, msg

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
        print("The question is analyzed")

    # Inserting the question to the DB
    questionCollection.insert_one(question)
    msg = "A new question is inserted"
    print(msg)
    print("---------------------------")

    return True, msg


'''
    Searching a question after analyzing it

    :param (str) questionBody: text of the question itself
    :param (Object) db: database object for db connection
'''
def findSimilarQuestions(questionBody, db):

    try:
        # Analyzing the question
        entity_tags, topics, categories = analyzeQuestion(questionBody)
        maxTopicScore = calculateMaxPossibleScore(topics)

        # Creating dict from input question topics
        topicsDict = {}
        for topic in topics:
            topicsDict[topic['label']] = topic['score']

        # DB collection
        questionCollection = db["questions"]

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

    :param (Object) db: database object for db connection
'''
def removeOnesWithoutAttrs(db):

    # DB collection
    questionCollection = db["questions"]

    query = { "$and": [{"topics": None}, {"entity_tags": None}, {"categories": None}] }
    x = questionCollection.delete_many(query)
