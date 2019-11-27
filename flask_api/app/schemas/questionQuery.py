from marshmallow import Schema, fields, validate

'''
    Schema for question queries
'''
class QuestionQuerySchema(Schema):

    logicalOp = fields.Str(required = True)
    body = fields.Str(required = False)
    source = fields.Dict(required = False)
    viewCount = fields.Dict(required = False)
    favCount = fields.Dict(required = False)
    entityTag = fields.Dict(required = False)
    topic = fields.Dict(required = False)
    category = fields.Dict(required = False)


'''
	Validating the question query using the schema above
'''

def validateQuestionQuery(data):

	errors = QuestionQuerySchema().validate(data)

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