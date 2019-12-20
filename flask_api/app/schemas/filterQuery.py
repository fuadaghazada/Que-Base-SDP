from marshmallow import Schema, fields, validate

from app.helpers.types import QuestionType

'''
    Schema for filter queries
'''
class FilterQuerySchema(Schema):

    body = fields.Str(required = True)
    source = fields.Dict(required = True)
    viewCount = fields.Dict(required = True)
    favCount = fields.Dict(required = True)
    sort = fields.Dict(required = True)

    entityTag = fields.Dict(required = False)
    topic = fields.Dict(required = False)
    category = fields.Dict(required = False)

    label = fields.Str(required = False)
    level = fields.Str(required = False)

'''
	Validating the filter query using the schema above
'''

def validateFilterQuery(data):

	errors = FilterQuerySchema().validate(data)

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
