from flask import Flask

from utils.configReader import getConfig
from controllers import questionController

'''
    Creating / Configuring the Flask app
'''

# Configuration settings
__config = getConfig()

# Flask app
app = Flask("Quesbase")

# Controllers
app.register_blueprint(questionController.bluePrint)

# Running the server
if __name__ == '__main__':
    app.run(host = __config['HOST'], port = __config['PORT'], debug = True)
