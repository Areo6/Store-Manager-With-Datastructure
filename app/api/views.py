from flask import Blueprint, request, json, jsonify
from api.validation import *
from api.models import Products, SaleOrder
from api.model_helper import *


mod = Blueprint("api", __name__)
product = Products()
sale = SaleOrder()
user = User()

@mod.route("/api/v2/signup", methods = ["POST"])
def create_attendant():
    """
    This endpoint is user by the admin to create an attendant
    """
    try:
        json.loads(request.get_data())
    except (ValueError, TypeError):
        return json_er("Bad request, your request should be in a dictionary format"), 400
    data = request.get_json(force=True)
    if not data:
        return json_er("Bad request, your request should be in a dictionary format"), 400
    print(len(data))
    if len(data) < 4:
        return json_er("Missing fields. Please make sure username, email and password are provided"),400
    if len(data) > 4:
        return json_er("Too many arguments. Only username, email and password are required"), 414
    if not "username" in data or not "email" in data or not "password" in data or not "user_role" in data:
        return json_er("Either username, email, password or user_role is missing. Please check the spelling"), 400
    validation_user = user_validation(data["username"], data["email"], data["password"], data["user_role"])
    if validation_user != "Valid":
        return json_er(validation_user), 417
    attendant = user.create_user(data["username"], data["email"], data["password"], data["user_role"])
    user_added = single_user(data["username"])
    return json_msg(attendant, "User", user_added), 201

@mod.route("/api/v2/login", methods = ["POST"])
def login():
    """
    TThis endpoint is used by the user to login
    """
    try:
        json.loads(request.get_data())
    except (ValueError, TypeError):
        return json_er("Bad request, your request should be in a dictionary format"), 400
    data = request.get_json(force=True)
    if not data:
        return json_er("Bad request, your request should be in a dictionary format"), 400
    print(len(data))
    if len(data) < 2:
        return json_er("Username or password missing"),400
    if len(data) > 2:
        return json_er("Too many arguments. Only Username and passord are required"), 414
    if not "username" in data or not "password" in data:
        return json_er("Username or password missing. Please check the spelling"), 400
    user_login = user_can_login(data["username"], data["password"])
    if user_login != "Valid":
        return user_login
    if is_user_exist(data["username"]):
        existing_user = user.login(data["username"])
        if existing_user["password"] == data["password"]:
            token =  jsonify({
                "token": "My token",
                "Message": "User successfully login"
            }), 201
            return token
        return json_er("Wrong password. Please try again")
    return json_er("User with name {} does not have an account. Please ask your admin to create one")

@mod.route("/api/v1/products", methods = ["GET"])
def get_products():
    """
    This endpoint allows the user to fetch all products
    """
    if is_products_empty():
            return json_ms("Oops! There no product added yet"), 200
    return json_msgs(product.get_all_products()), 200

@mod.route("/api/v1/products", methods = ["POST"])
def create_product():
    """
    This endpoint is allows the admin to add a new product to the store
    """
    try:
        json.loads(request.get_data())
    except (ValueError, TypeError):
        return json_er("Bad request, your request should be a dictionary"), 400
    data = request.get_json(force=True)
    if not data:
        return json_er("Bad request, your request should be a dictionary"), 400
    print(len(data))
    if len(data) < 4:
        return json_er("Insuficiant number of inputs. make sure all the fields are inluded"),400
    if len(data) > 4:
        return json_er("Too many arguments. Only name, price, quantity, quantity_allowed, and category are required"), 414
    if not "product_name" in data or not "price" in data or not "quantity" in data or not "min_qty_allowed" in data:
        return json_er("Pease make sure name, price, quantity, quantity_allowed are in the request"), 400
    prod_validation = product_validation(data["product_name"],data["price"],data["quantity"], data["min_qty_allowed"])
    if prod_validation != "Valid":
        return json_er(prod_validation), 417
    prod = product.add_product(data["product_name"],data["price"],data["quantity"], data["min_qty_allowed"])
    product_added = single_product(data["product_name"])
    return json_msg(prod, "Product", product_added), 201

@mod.route("/api/v1/products/<id>", methods = ["GET"])
def get_product(id):
    """
    This endpoint allows the user fetch a specific product
    """
    try:
        id = int(id)
    except(ValueError, TypeError):
        return json_er("Bad request. Id should be an integer"), 405
    if valid_id(id) != "Valid":
        return json_er("Invalid Id. Must be a positive number"), 400
    product_validation = get_product_id_validation(id)
    if product_validation != "Valid":
        return json_er(product_validation), 404
    return json_mesage(product.get_product(id)), 200

@mod.route("/api/v1/sales", methods = ["POST"])
def create_sale_order():
    """
    This endpoint allows the store attendant to create a sale record
    """
    try:
        json.loads(request.get_data())
    except (ValueError, TypeError):
        return json_er("Bad request, your request should be a dictionary"), 400
    data = request.get_json(force=True)
    if not data:
        return json_er("Bad request, your request should be a dictionary"), 400
    if len(data) < 3:
        return json_er("Insuficiant number of inputs. please make sure all the fields are included"), 400
    if len(data) > 3:
        return json_er("Too many arguments. only product_id, quantity and attendant_name are required"), 414
    if not "product_id" in data or not "quantity" in data or not "attendant_name" in data: 
        return json_er("Please make sure product_id, quantity and attendant_name are included int he request")
    order_validation = sale_validation(data["product_id"], data["quantity"], data["attendant_name"])
    if order_validation != "Valid":
        return json_er(order_validation), 417
    order = sale.add_sale_order(data["product_id"], data["quantity"], data["attendant_name"])
    order_added = single_sale(data["product_id"])
    return json_msg(order, "Sale", order_added), 201

@mod.route("/api/v1/sales", methods = ["GET"])
def get_all_sales():
    """
    This enpoint allows the owner/admin to view all sales records available
    """
    if is_sales_empty():
        return json_ms("Oh oh! It looks like there is are no sale orders made yet"), 200
    return json_mesages("Sales", sale.get_all_sales()), 200

@mod.route("/api/v1/sales/<id>", methods = ["GET"])
def get_sale(id):
    """
    This endpoint allows the user to fetch a specific sale record
    """
    try:
        id = int(id)
    except(ValueError, TypeError):
        return json_er("Bad request. Id should be an integer"), 405
    if valid_id(id) != "Valid":
        return json_er("Invalid Id. Must be a positive number"), 400
    sale_validation = get_sale_id_validation(id)
    if sale_validation != "Valid":
        return json_er(sale_validation), 404
    return json_mesages("Sale order", sale.get_sale_record(id)), 200
