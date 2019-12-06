from marshmallow import Schema, fields, validate

'''
    Schema for filter queries
'''
class FilterQuerySchema(Schema):

    body = fields.Str(required = True)
    source = fields.Dict(required = True)
    viewCount = fields.Dict(required = True)
    favCount = fields.Dict(required = True)
    entityTag = fields.Dict(required = True)
    topic = fields.Dict(required = True)
    category = fields.Dict(required = True)
    sort = fields.Dict(required = True)


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
