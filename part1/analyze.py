from TextClassifier import TextClassifier
from configReader import getConfig

# the Text Classifier
config = getConfig()
classifier = TextClassifier(config['TEXT_RAZOR_API_KEY'])


'''
    Analyzing the question by extracting:
        - entity_tags
        - topics
        - categories

    :param (str) questionBody: question text itself
    :return (tuple): entity_tags, topics, categories
'''
def analyzeQuestion(questionBody, thresholds = {"entity_tags": 0.0, "topics": 0.7,  "categories": 0.35}):

    properties = {
      "text_to_analyze": questionBody,
      "entity_tags": {
        "extract_entity_tags": True,
        "relevance_threshold": thresholds['entity_tags']
      },
      "topics": {
        "extract_topics": True,
        "score_threshold": thresholds['topics']
      },
      "categories": {
        "extract_categories": True,
        "score_threshold": thresholds['categories']
      }
    }

    # Classification process...
    classificationResult = classifier.analyze(properties)

    # Fields
    entity_tags = classificationResult["entity_tags"]
    topics = classificationResult["topics"]
    categories = classificationResult["categories"]

    return entity_tags, topics, categories
