class CustomQueryGenerator:

    def __init__(self, baseOp = "and"):

        # Filtering conditions are combined using a logical operator
        # <FILTER_1>  LOGICAL_OPERATOR  <FILTER_2>  LOGICAL_OPERATOR  ...  <FILTER_N>
        # e.g. (topic is conformity) AND (viewCount > 20)

        # list of individual filters that will be connected by logical operators
        self.conditions = []

        # The query itself (represented by a dictionary)
        self.query = {}

        # Base Logical operator
        self.baseOp = baseOp

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


    def addSourceField(self, fields):

        # In the source object, there are the following fields
        sourceFields = fields.keys()

        # A flag indicating whether any filtering is done here
        # (If all sourceFields are empty strings, no filtering is needed and the flag remains "False")
        isSourceFilterUsed = False

        # Dictionary object storing the subquery
        sourceQuery = dict()

        # For each field in the "source" object
        for field in sourceFields:

            # If the field is not equal to empty string, add that field to the query
            if fields[field] != "":

                name = "source." + field
                sourceQuery[name] = {
                    "$regex": fields[field],
                    "$options": "i"
                }

                isSourceFilterUsed = True

        if isSourceFilterUsed:
            self.conditions.append(sourceQuery)


    def addIdFields(self, ids):
        if len(ids) > 0:
            query = {"_id": {"$in": ids}}
            self.conditions.append(query)


    @staticmethod
    def appendTwoQueries(queryDict1, queryDict2):

        query1Keys = list(queryDict1.keys())
        query2Keys = list(queryDict2.keys())

        query1Key, query2Key = None, None

        if len(query1Keys) == 1:
            query1Key = query1Keys[0]
        if len(query2Keys) == 1:
            query2Key = query2Keys[0]

        if (query1Key and query2Key) and query1Key == query2Key:

            mergedQueryDict = {query1Key: []}

            mergedQueryDict[query1Key] += queryDict1[query1Key]
            mergedQueryDict[query2Key] += queryDict2[query2Key]

            return mergedQueryDict
        else:
            return None


    def getCompleteQuery(self):

        # Checking the base operator
        validation = checkOperator(self.baseOp, type = "logical")
        if not validation:
            self.error = True

        if not self.error:

            if len(self.conditions) > 0:
                # Prepare the query
                operator = f'${self.baseOp}'
                self.query[operator] = self.conditions
            else:
                self.query = {}

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
