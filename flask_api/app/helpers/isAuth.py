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
                }), 400

            # Decoding
            status, msg, data = decode_token(token)

            if status is True:
                # Continue...
                return f(data, *args, **kwargs)
            else:
                return jsonify({
                    "success": False,
                    "message": msg
                }), 400

        return wrapped
    return decorator
