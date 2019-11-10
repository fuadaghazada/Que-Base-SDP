from flask import Flask
from flask_bcrypt import Bcrypt

from utils.configReader import getConfig
from utils.JSONEncoder import JSONEncoder

from controllers import questionController, authController


'''
    Creating / Configuring the Flask app
'''

# Configuration settings
__config = getConfig()

# Flask app
app = Flask("Quesbase")

# App Configurations
app.json_encoder = JSONEncoder

encrypter = Bcrypt(app)

# Controllers
app.register_blueprint(questionController.bluePrint)
app.register_blueprint(authController.bluePrint)
