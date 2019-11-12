from flask import current_app as app
from flask_pymongo import PyMongo

from app.utils.configReader import getConfig

# DB
db = None

# Configuration
__config = getConfig()

'''
    Connecting to the Database
'''

def getDb():

    global db

    if db is None:
        app.config['MONGO_DBNAME'] = __config['DB_NAME']
        app.config['MONGO_URI'] = __config['DB_URL'] + __config['DB_NAME']

        try:
            # DB connection
            mongo = PyMongo(app)

            return mongo.db

        except Exception as e:
            print("[ERROR] DB Connection cannot be established!")
            print(e)
            return None

    else:
        return db
