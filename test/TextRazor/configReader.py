import sys
import json

configOptions = None
configFileName = sys.argv[1]

'''
    Getting the configuration options from the config file
'''

def getConfig():

    global configOptions

    if configOptions is None:
        try:
            with open(configFileName, "r") as readFile:
                configOptions = json.load(readFile)
                return configOptions
        except Exception as e:
            raise Exception("Cannot read the config file")

    else:
        return configOptions
