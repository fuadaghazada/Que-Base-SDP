from marshmallow import Schema, fields, validate

'''
    Post schema for validation
'''

class PostSchema(Schema):

    # Fields
    userId = fields.Str(required = True)
    message = fields.Str(required = True)
    questionId = fields.Str(required = False)
    questionTitle = fields.Str(required = True)


'''
    Validating the given data via the predefined post schema
'''

def validatePost(data):

    # Validation...
    errors = PostSchema().validate(data)

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
