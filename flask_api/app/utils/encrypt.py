from werkzeug.security import generate_password_hash, check_password_hash


'''
    Hash the password

    :param: (str) password - password to be hashed
'''

def hashPassword(password):
    try:
        return generate_password_hash(password)
    except Exception as e:
        print("Password failed to be hashed")
        raise e
        return password


'''
    Check the hashed password

    :param: (str) userPassword - hashed user password from db
    :param: (str) password - password to be checked
'''

def validatePassword(userPassword, password):
    try:
        return check_password_hash(userPassword, password)
    except Exception as e:
        print("Password cannot be validated")
        raise e
        return False
