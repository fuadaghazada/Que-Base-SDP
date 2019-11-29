class CustomQueryGenerator:

    def __init__(self):

        # Filtering conditions are combined using a logical operator
        # <FILTER_1>  LOGICAL_OPERATOR  <FILTER_2>  LOGICAL_OPERATOR  ...  <FILTER_N>
        # e.g. (topic is conformity) AND (viewCount > 20)

        # list of individual filters that will be connected by logical operators
        self.conditions = []

        # The query itself (represented by a dictionary)
        self.query = {}

        # To determine if there is an erroneous case
        self.error = False


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

        # Checking the operator
        validation = checkOperator(comparisonOperator, type = "comparison")
        if not validation:
            self.error = True
            return

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

        # Checking the operator
        validation = checkOperator(logicalOp, type = "logical")
        if not validation:
            self.error = True
            return

        elemMatchquery = {f"${logicalOp}": []}
        for string in stringsToMatch:
            elemMatchquery[f"${logicalOp}"].append({fieldName: { "$elemMatch": { "label": { "$regex": string, "$options": "i" }}}})

        if len(stringsToMatch) == 0:
            return
        else:
            self.conditions.append(elemMatchquery)


    def addSourceField(self, fieldValues):

        reference = fieldValues["reference"]
        university = fieldValues["university"]
        course = fieldValues["course"]

        sourceQuery = {
            "source.reference": {"$regex": reference, "$options": "i"},
            "source.university": {"$regex": university, "$options": "i"},
            "source.course": {"$regex": course, "$options": "i"}
        }
        self.conditions.append(sourceQuery)


    def getCompleteQuery(self):

        if len(self.conditions) > 0 and not self.error:

            # Prepare the query
            operator = '$and'
            self.query[operator] = self.conditions
            print(self.query)
            return True, self.query

        return False, None

# ----------------------------------------------------------------------------------------------------------------

'''
    Helper methods for validating operators (logical, comparison)
'''

def checkOperator(operatorName, type):

    if type == "logical":
        return operatorName == "or" or operatorName == "and"
    elif type == "comparison":
        return operatorName == "gt" or operatorName == "gte" or operatorName == "lt" or operatorName == "lte" or operatorName == "eq"
    else:
        return False
