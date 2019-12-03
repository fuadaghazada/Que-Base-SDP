from flask import Flask
from flask_cors import CORS

from .utils.configReader import getConfig
from .utils.JSONEncoder import JSONEncoder

from .controllers import *

'''
    Creating / Configuring the Flask app
'''

# Configuration settings
config = getConfig()

# Flask app
app = Flask("Quesbase")

# App Configurations
app.json_encoder = JSONEncoder
cors = CORS(app)

# Controllers
app.register_blueprint(scQuestionBluePrint)
app.register_blueprint(algoQuestionBluePrint)
app.register_blueprint(questionBluePrint)
app.register_blueprint(authBluePrint)
app.register_blueprint(userBluePrint)
app.register_blueprint(adminBluePrint)
