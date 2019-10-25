import pymongo
from configReader import getConfig

mydb = None
config = getConfig()


'''
    Connecting to the Database
'''

def getDb():

    global mydb

    if mydb is None:
        myclient = pymongo.MongoClient(config["DB_URL"])
        mydb = myclient[config["DB_NAME"]]

        return mydb
    else:
        return mydb
