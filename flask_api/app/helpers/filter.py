from app.helpers.query import CustomQueryGenerator
from app.helpers.types import QuestionType

'''
    Creating filter query from the request data (json)

'''
def createFilterQuery(attr, type = QuestionType.SOC):
    # Empty
    query = CustomQueryGenerator()

    # Extract the relevant fields from the request
    query.addStringField('body', attr['body'], elastic=True)
    query.addNumberComparisonField('viewCount', attr['viewCount'])
    query.addNumberComparisonField('favCount', attr['favCount'])
    query.addSourceField(attr['source'])

    if type == QuestionType.SOC:
        query.addElemMatchFields('entity_tags', attr['entityTag'])
        query.addElemMatchFields('topics', attr['topic'])
        query.addElemMatchFields('categories', attr['category'])

    elif type == QuestionType.ALGO:
        query.addStringField('level', attr['level'])
        query.addElemMatchFields('labels', attr['labels'])

    sortingProperties = attr['sort']
    sortingAttr = sortingProperties['attr']
    sortOrder = sortingProperties['order']

    # Get the final query
    queryStatus, queryDict = query.getCompleteQuery()

    if queryStatus:
        return (queryDict, sortingAttr, sortOrder), "Query is generated"
    else:
        return None, "Invalid query"
