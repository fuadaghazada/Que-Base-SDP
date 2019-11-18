from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from marshmallow.validate import Length, Range, Email, Equal

'''
    User schema for validation (Registration)
'''

class RegisterSchema(Schema):

    # Fields
    firstname = fields.Str(required = True, validate = Length(min = 1, max = 50))
    lastname = fields.Str(required = True, validate = Length(min = 1, max = 50))
    username = fields.Str(required = True, validate = Length(min = 6, max = 50))
    email = fields.Email(required = True, error = "Not a valid email address")
    password = fields.Str(required = True, validate = Length(min = 1, max = 50))
    confirmPassword = fields.Str(required = True)

    @validates_schema
    def checkConfirmPassword(self, instance, **kwargs):
        if instance['password'] != instance['confirmPassword']:
            raise ValidationError("No matching password")


'''
    User schema for validation (Login)
'''

class LoginSchema(Schema):

    # Fields
    email = fields.Email(required = True, error = "Not a valid email address")
    password = fields.Str(required = True, validate = Length(min = 1, max = 50))


'''
    Validating the given data via the predefined user schema
'''

def validateUser(data, isLogin = False):

    # Validation...
    errors = RegisterSchema().validate(data) if isLogin is False else LoginSchema().validate(data)

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
