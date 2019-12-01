import math
from copy import deepcopy
from bson.objectid import ObjectId

from app.utils.db import getDb

from app.helpers.constant import LIMIT

'''
    Generic model class
'''
class Model():
    '''
        Creating a model

        :param: (dict) obj - object contains the properties
    '''
    def __init__(self, obj, collectionName):
        self.init(obj, collectionName)


    '''
        Initializing the object properties

        :param: (dict) obj - object contains the properties
        :param: collectionName - name of the collection in the db for the model
    '''
    def init(self, obj, collectionName):

        # Getting by some key
        keys = list(obj.keys())
        key = keys[0] if len(keys) == 1 else None

        if key:
            db = getDb()
            value = obj[key] if key != "_id" else ObjectId(obj[key])

            data = db[collectionName].find_one({key: value})

            if data:
                properties = dict(data).keys()
                for property in properties:
                    setattr(self, property, data[property])

    '''
        Getting the data from model object
    '''
    def data(self):
        return vars(self)


    '''
        Static method for returning the result with the given query

        :param: collectionName - collection name of in the db
        :param: query - the given query (Mongo)
        :param: sortingAttr - attribute/field for sorting (default by id)
        :param: sortOrder - order for sorting (1 - asc, -1 - desc)
        :param: pageNumber - page number for pagination
    '''
    @staticmethod
    def find(collectionName, query, sortingAttr = "_id", sortOrder = 1, pageNumber = 1):
        db = getDb()

        # Getting the question with the parameters: pagination and sort
        offset = (pageNumber - 1) * LIMIT
        cursor = db[collectionName].find(query)

        # TODO: try removing or update the try/except statement with better version
        # If sorting Attribute is not a valid one; do not sort
        try:
            if sortingAttr != "" or sortingAttr is not None:
                cursor = cursor.sort(sortingAttr, sortOrder)
        except Exception as e:
            pass

        count = cursor.count()
        results = cursor.skip(offset).limit(LIMIT)
        numberOfPages = math.ceil(count / LIMIT)

        return {
            "data": list(results),
            "numberOfPages": numberOfPages
        }


    '''
        Updating the model properties

        :param: updateValues - new value for update
        :param: collectionName - name of the collection in the db for the model
    '''
    def update_one(self, updateValues, collectionName):
        db = getDb()

        if self._id:
            db[collectionName].update_one({"_id": ObjectId(self._id)}, {"$set": updateValues})
            self.init(vars(self), collectionName)

            return True

        return False
