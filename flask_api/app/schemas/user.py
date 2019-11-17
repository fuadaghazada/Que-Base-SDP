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
            "type": "string",
            "minLength": 1
        },
        "lastname": {
            "type": "string",
            "minLength": 1
        },
        "username": {
            "type": "string",
            "minLength": 6
        },
        "email": {
            "type": "string",
            "pattern": "^[a-z0-9\._%+!$&*=^|~#%{}/\-]+@([a-z0-9\-]+\.){1,}([a-z]{2,22})$"
        },
        "password": {
            "type": "string",
            "minLength": 6
        },
        "confirmPassword": {
            "type": "string"
        },
    },
    "required": ["firstname", "lastname", "username", "email", "password", "confirmPassword"],
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

            # Confirming the password
            if data["confirmPassword"] != data["password"]:
                raise ValidationError("No matching passwords")

    except ValidationError as e:
        return {
            'success': False,
            'message': str(e.message)
        }
    except SchemaError as e:
        return {
            'success': False,
            'message': str(e.message)
        }

    # Success!
    return {
        'success': True,
        'data': data
    }
