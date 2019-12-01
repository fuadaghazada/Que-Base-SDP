from app.helpers.query import CustomQueryGenerator


'''
    Creating filter query from the request data (json)

'''
def createFilterQuery(attr):
    # Empty
    query = CustomQueryGenerator()

    # Extract the relevant fields from the request
    query.addStringField('body', attr['body'], elastic=True)
    query.addNumberComparisonField('viewCount', attr['viewCount'])
    query.addNumberComparisonField('favCount', attr['favCount'])
    query.addSourceField(attr['source'])
    query.addElemMatchFields('entity_tags', attr['entityTag'])
    query.addElemMatchFields('topics', attr['topic'])
    query.addElemMatchFields('categories', attr['category'])

    sortingProperties = attr['sort']
    sortingAttr = sortingProperties['attr']
    sortOrder = sortingProperties['order']

    # Get the final query
    queryStatus, queryDict = query.getCompleteQuery()

    if queryStatus:
        return (queryDict, sortingAttr, sortOrder), "Query is generated"
    else:
        return None, "Invalid query"
