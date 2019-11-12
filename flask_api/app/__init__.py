from flask import Flask

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

# Controllers
app.register_blueprint(questionBluePrint)
app.register_blueprint(userBluePrint)
