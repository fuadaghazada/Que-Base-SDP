from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError

'''
    Schema of Question object for validation
'''

questionSchema = {
    "type": "object",
    "properties": {
        "body": {
            "type": "string",
        }
    },
    "required": ["body"],
    "additionalProperties": False
}


'''
    Validating the question data
'''

def validateQuestion(data):
    try:
        # Validating here...
        validate(data, questionSchema)

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
