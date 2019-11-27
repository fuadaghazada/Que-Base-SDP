class CustomQueryGenerator:
    
    def __init__(self, logicalOperator):

        # Filtering conditions are combined using a logical operator
        # <FILTER_1>  LOGICAL_OPERATOR  <FILTER_2>  LOGICAL_OPERATOR  ...  <FILTER_N>
        # e.g. (topic is conformity) AND (viewCount > 20)

        # Logical operator to use (one of "and" or "or")
        self.logicalOperator = logicalOperator

        # list of individual filters that will be connected by logical operators
        self.conditions = []

        # The query itself (represented by a dictionary)
        self.query = {}


    def addStringField(self, fieldName, fieldValue, elastic=False):

        # Empty string implies that this filter is disabled
        if fieldValue == "":
            return
        else:
            if elastic:
                self.conditions.append({ "$text": { "$search": fieldValue } })
            else:
                self.conditions.append({ fieldName: fieldValue })


    def addNumberComparisonField(self, fieldName, comparisonSpecs):

        comparisonOperator = comparisonSpecs['comparisonOperator']  # one of "lt", "lte", gt", "gte" or "eq"
        value = comparisonSpecs['value']

        # -1 means that this filter is disabled
        if value == -1:
            return
        else:
            comparisonOp = '$' + comparisonOperator
            self.conditions.append({fieldName: { comparisonOp: value }})


    def addElemMatchFields(self, fieldName, fieldValues):

        logicalOp = fieldValues['logicalOp']
        stringsToMatch = fieldValues['stringsToMatch']

        elemMatchquery = {f"${logicalOp}": []}
        for string in stringsToMatch:
            elemMatchquery[f"${logicalOp}"].append({fieldName: { "$elemMatch": { "label": { "$regex": string, "$options": "i" }}}})

        if len(stringsToMatch) == 0:
            return
        else:
            self.conditions.append(elemMatchquery)


    def getCompleteQuery(self):

        if len(self.conditions) > 0:
        
            # Prepare the query
            operator = '$' + self.logicalOperator
            self.query[operator] = self.conditions

            return True, self.query

        return False, None
