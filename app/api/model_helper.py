from api.validation import *
from api.db import Database
from api.models import *


db = Database()
cursor = db.cur
produc = Products()
sale_order = SaleOrder()
users = User()

def fetch_user(username):
    usr = users.search_user_name(username)
    return usr

def user_validation(username, email, password, user_role):
    """
    This function checks if the fields for user provided are valid
    """
    if is_valid_username(username) != "Valid":
        return is_valid_username(username)
    if is_valid_email(email) != "Valid":
        return is_password(email)
    if is_valid_password(password) != "Valid":
        return is_valid_password(password)
    if is_valid_role(user_role) != "Valid":
        return is_valid_role(user_role)
    query = ("""SELECT username FROM users WHERE username = '{}'""".format(username))
    cursor.execute(query)
    name = cursor.fetchone()
    if name:
        return "Name {} alredy taken. Please choose a different one".format(username)
    return "Valid"

def user_can_login(username, password):
    """
    This function checks if the user prpovided valid data to login
    """
    if is_valid_username(username) != "Valid":
        return is_valid_username(username)
    if is_valid_password(password) != "Valid":
        return is_valid_password(password)
    return "Valid"
    
def is_user_exist(username):
    query = ("""SELECT username FROM users WHERE username = '{}'""".format(username))
    cursor.execute(query)
    user = cursor.fetchone()
    if user:
        return True
    else:
        return False

def is_email_exist(email):
    query = ("""SELECT * FROM users WHERE email = '{}'""".format(email))
    cursor.execute(query)
    email = cursor.fetchone()
    if email:
        return True
    else:
        return False

def single_user(username):
    """
    This function is used to fetch a single sale
    """
    query = ("""SELECT user_id FROM users WHERE username = '{}'""".format(username))
    cursor.execute(query)
    id = cursor.fetchone()
    query = ("""SELECT username FROM users WHERE username = '{}'""".format(username))
    cursor.execute(query)
    name = cursor.fetchone()
    attendant = {
        "user_id": id["user_id"],
        "username": name["username"]
    }
    return attendant

def single_usr(user_id):
    """
    This function is used to fetch a single sale
    """
    query = ("""SELECT user_id FROM users WHERE user_id = '{}'""".format(user_id))
    cursor.execute(query)
    id = cursor.fetchone()
    query = ("""SELECT username FROM users WHERE user_id = '{}'""".format(user_id))
    cursor.execute(query)
    name = cursor.fetchone()
    attendant = {
        "user_id": id["user_id"],
        "username": name["username"]
    }
    return attendant

def product_validation(name, price, qty_available, min_qty_allowed):
        """
        This function is used to validate a product
        """
        if valid_name(name) != "Valid":
            return valid_name(name)
        if valid_price(price) != "Valid":
            return valid_price(price)
        if valid_quantity(qty_available) != "Valid":
            return valid_quantity(qty_available)
        if valid_quantity(min_qty_allowed) != "Valid":
            return valid_quantity(min_qty_allowed)
        if min_qty_allowed > qty_available:
            return "Minimum quantity can't be greater than the quantity available in store"
        query = ("""SELECT product_name FROM products WHERE product_name = '{}'""".format(name))
        cursor.execute(query)
        product = cursor.fetchone()
        if product:
            return "Product with name {} already exists. Choose another name".format(name)
        return "Valid"

def product_update_validation(id,name, price, qty_available, min_qty_allowed):
        """
        This function is used to validate a product
        """
        query = ("""SELECT * FROM products WHERE product_id = '{}'""".format(id))
        cursor.execute(query)
        product = cursor.fetchone()
        if not product:
            return "Product with id {} does not exist. Choose another one".format(id)
        if valid_name(name) != "Valid":
            return valid_name(name)
        if valid_price(price) != "Valid":
            return valid_price(price)
        if valid_quantity(qty_available) != "Valid":
            return valid_quantity(qty_available)
        if valid_quantity(min_qty_allowed) != "Valid":
            return valid_quantity(min_qty_allowed)
        if min_qty_allowed > qty_available:
            return "Minimum quantity can't be greater than the quantity available in store"
        query = ("""SELECT product_name FROM products WHERE product_name = '{}'""".format(name))
        cursor.execute(query)
        product = cursor.fetchone()
        if product:
            return "Product with name {} already exists. Choose another name".format(name)
        return "Valid"    

def single_product(product_name):
    """
    This function is used to fetch a single product
    """
    query = ("""SELECT product_id FROM products WHERE product_name = '{}'""".format(product_name))
    cursor.execute(query)
    id = cursor.fetchone()
    query = ("""SELECT product_name FROM products WHERE product_name = '{}'""".format(product_name))
    cursor.execute(query)
    name = cursor.fetchone()
    product = {
        "product_id": id["product_id"],
        "name": name["product_name"]
    }
    return product

def single_product_by_id(product_id):
    """
    This function is used to fetch a single product
    """
    query = ("""SELECT product_id FROM products WHERE product_id = '{}'""".format(product_id))
    cursor.execute(query)
    id = cursor.fetchone()
    query = ("""SELECT product_name FROM products WHERE product_id = '{}'""".format(product_id))
    cursor.execute(query)
    name = cursor.fetchone()
    product = {
        "product_id": id["product_id"],
        "name": name["product_name"]
    }
    return product

def single_sale(product_id):
    """
    This function is used to fetch a single sale
    """
    query = ("""SELECT sale_id FROM sales WHERE product_id = '{}'""".format(product_id))
    cursor.execute(query)
    id = cursor.fetchone()
    query = ("""SELECT product_name FROM products WHERE product_id = '{}'""".format(product_id))
    cursor.execute(query)
    product_name = cursor.fetchone()
    sale = {
        "product_id": id["sale_id"],
        "name": product_name["product_name"]
    }
    return sale

def get_product_id_validation(id):
    """
    This function checks if provided id exists in the database
    """
    if valid_id(id) != "Valid":
            return valid_id(id)
    product = produc.get_product(id)
    if not product:
        return "Product with id {} not found".format(id)
    return "Valid" 

def sale_validation(product_id, quantity, attendant_name):
        """
        This function is used to validate a product
        """
        if valid_id(product_id) != "Valid":
            return valid_id(prod_id)
        if valid_quantity(quantity) != "Valid":
            return valid_quantity(quantity)
        if valid_name(attendant_name) != "Valid":
            return valid_name(attendant_name)
        query = ("""SELECT product_id FROM products WHERE product_id = '{}'""".format(product_id))
        cursor.execute(query)
        product = cursor.fetchone()
        if not product:
            return "Product with id {} does not exist"
        return "Valid"

def is_products_empty():
    query = ("""SELECT * FROM products;""")
    cursor.execute(query)
    product = cursor.fetchall()
    if product:
        return False
    else:
        return True
    
def is_sales_empty():
    query = ("""SELECT * FROM sales;""")
    cursor.execute(query)
    sale = cursor.fetchall()
    if sale:
        return False
    else:
        return True
    
def get_sale_id_validation(id):
    """
    This function checks if provided id exists in the database
    """
    if valid_id(id) != "Valid":
            return valid_id(id)
    sale = sale_order.get_sale_record(id)
    if not sale:
        return "Sale with id {} not found. put a valid id".format(id)
    return "Valid"