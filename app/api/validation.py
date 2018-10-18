from flask import jsonify


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

def json_msg(header,msg):
    """
    This method returns a message in json format
    """
    return jsonify({header:msg})
