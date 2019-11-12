import jwt
import datetime

from .configReader import getConfig
from .JSONEncoder import customEncode

# Configuration
__config = getConfig()
secretKey = __config['SECRET_KEY']



'''
    Generates the Auth Token

    :return: (string) token
'''

def encode_token(data, algorithm='HS256', timeDelta=datetime.timedelta(days=0, hours=1)):

    try:
        payload = {
            'exp': datetime.datetime.utcnow() + timeDelta,
            'iat': datetime.datetime.utcnow(),
            'sub': customEncode(data)
        }
        return jwt.encode(
            payload,
            secretKey,
            algorithm=algorithm
        )
    except Exception as e:
        return e


'''
    Validates the auth token

    :param (string) token:
    :return: (tuple) (status, msg, data)
'''

def decode_token(token):

    try:
        payload = jwt.decode(token, secretKey)

        return True, "Decode is successful", payload['sub']

    except jwt.ExpiredSignatureError as e:
        return False, "Token has been expired", None

    except jwt.InvalidTokenError as e:
        return False, "Invalid token", None
