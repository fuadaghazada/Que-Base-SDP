from copy import deepcopy

from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError

'''
    Schema of User object for validation
'''

userSchema = {
    "type": "object",
    "properties": {
        "firstname": {
            "type": "string"
        },
        "lastname": {
            "type": "string"
        },
        "username": {
            "type": "string",
            "minLength": 6
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "password": {
            "type": "string",
            "minLength": 6
        }
    },
    "required": ["firstname", "lastname", "username", "email", "password"],
    "additionalProperties": True
}

# Login schema: only email and password is required
_loginSchema = deepcopy(userSchema)
_loginSchema["required"] = ["email", "password"]
del _loginSchema["properties"]["password"]["minLength"]

'''
    Validating the question data
'''

def validateUser(data, isLogin = False):
    try:
        # Validating here...
        if isLogin is True:
            validate(data, _loginSchema)
        else:
            validate(data, userSchema)

    except ValidationError as e:
        return {
            'success': False,
            'message': str(e)
        }
    except SchemaError as e:
        return {
            'success': False,
            'message': str(e)
        }

    # Success!
    return {
        'success': True,
        'data': data
    }
