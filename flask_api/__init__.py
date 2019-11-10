from utils.configReader import getConfig
from app import app

# Config
__config = getConfig()

# Running the server
if __name__ == '__main__':
    app.run(host = __config['HOST'], port = __config['PORT'], debug = True)
