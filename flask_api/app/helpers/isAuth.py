from flask import jsonify
from functools import wraps

from app.utils.token import decode_token

'''
    Decorator for checking the authentication in the requests
'''

def isAuth(request):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):

            # Authorization token from headers
            token = request.headers.get('Authorization')

            # Check conditions...
            if token is None:
                return jsonify({
                    "success": False,
                    "message": "Authentication is required"
                })

            # Decoding
            status, msg, data = decode_token(token)
            
            if status is True:
                # Continue...
                return f(data, *args, **kwargs)
            else:
                return jsonify({
                    "success": False,
                    "message": msg
                })

        return wrapped
    return decorator


'''
    Simple and funny admin decorator/middleware
'''

def isAdmin(request):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):

            isAdmin = request.headers.get('Admin')

            if isAdmin:
                # Continue...
                return f(*args, **kwargs)
            else:
                return jsonify({
                    "success": False,
                    "message": "You are not an admin"
                })

        return wrapped
    return decorator
