from flask import jsonify
import re
import string


def is_valid_username(username):
    """
    This function checks the validity of the input Name.
    """
    if not isinstance(username, str):
        return "Bad input. Name should be a string"
    if len(username.strip()) == 0:
        return "Name can't be empty. Please enter a valid name"
    elif len(username.strip()) < 3:
        return "Invalid Name. Name must be at least 3 characters"
    pattern = re.match('^[^.]*[a-zA-Z]$', username)
    if not pattern:
        return "Invalid Name. Name must not contain special characters"
    else:
        return "Valid"

def is_valid_role(user_role):
    if valid_name(user_role) != "Valid":
        return valid_name(user_role)
    if user_role == "admin" or user_role == "attendant":
        return "Valid"
    return "Invalid"
    
def is_valid_email(email):
    """
    This function checks the validity of email.
    """
    is_valid = re.search(r"[\w-]+@[\w-]+\.+", email)
    if not is_valid:
        return "Invalid email. Email should be of format 'john12@gmail.com'"
    else:
        return "Valid"

def is_valid_password(password):
    """
    This function checks the validity of a password
    """
    if not isinstance(password, str):
        return "Invalid input. Password must be a string of characters"
    if len(password) < 6:
        return "Invalid password. Password must be at least 6 characters long"
    return "Valid"
    # upper, lower, symbol, digit = False, False, False, False
    # for char in password:
    #     if char in string.ascii_uppercase:
    #         upper = True
    #     elif char in string.ascii_lowercase:
    #         lower = True
    #     elif char in string.digits:
    #         digit = True
        # elif char in string.punctuation + ' \t\r\x0b\x0c':
        #     symbol = True
    # if upper == True and lower == True and digit == True:
        
    # else:
    #     return "Weak password. Password must contain at least one upper case, lower case and a special caracter"

def valid_name(name):
    """
    This function checks if the given name is a valid name
    """
    if not isinstance(name, str):
        return "Bad input. Name should be a string"
    if len(name.strip()) == 0:
        return "Name can't be empty. Please enter a valid name"
    elif len(name.strip()) < 3:
        return "Invalid Name. Name must be at least 3 characters long"
    else:
        return "Valid"
        
def valid_price(price):
    """
    This function checks if the given price is a valid price
    """
    if not isinstance(price, int):
        return "Bad input. price should be an integer"
    if price <= 0:
        return "Invalid price. Price must be a number greater than 0"
    return "Valid"

def valid_quantity(qty):
    """
    This function checks if the given quantity in store is valid.
    """
    if not isinstance(qty, int):
        return "Invalid quantity. Quantitiy must be a number"
    if qty < 0:
        return "Invalid quantity. Qty must be greater than 0"
    return "Valid"

def valid_category(category):
    """
    This function checks if the given category is valid
    """
    if not isinstance(category, str):
        return "Invalid format. Category must be a string"
    if len(category.strip()) == 0:
        return "Invalid category. Category can't be empty"
    if len(category.strip()) < 3:
        return "Invalid category. Category must be at least 3 characters long"
    return "Valid"

def valid_id(id):
    """
    This function checks if the given id is valid
    """
    if not isinstance(id, int):
            return "Invalid id. ID must be an integer number"
    if id <= 0:
        return "Invalid id. Id must be a positive number"
    return "Valid"

def json_er(msg):
    """
    This method returns an error message in json format
    """
    return jsonify({"Error": msg})

def json_msg(msg, some, data):
    """
    This method returns a message in json format
    """
    return jsonify({
        "Message": msg,
        some: data,
    })

def json_mesage(data):
    return jsonify({
        "User": data
    })

def json_ms(msg):
    return jsonify({"Message" : msg})

def json_mesages(msg, data):
    return jsonify({
        msg: data
    })