from marshmallow import Schema, fields, validate

'''
    User schema for validation (Registration)
'''

class QuestionSchema(Schema):

    # Fields
    body = fields.Str(required = True)


'''
    Validating the given data via the predefined question schema
'''

def validateQuestion(data):

    # Validation...
    errors = QuestionSchema().validate(data)

    if errors:
        return {
            'success': False,
            'message': str(errors)
        }
    else:
        return {
            'success': True,
            'data': data
        }
