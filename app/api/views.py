from flask import Blueprint, request, json, jsonify
from .validation import *
from .models import Products, SaleOrder
from .model_helper import *
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime


mod = Blueprint("api", __name__)
product = Products()
sale = SaleOrder()
user = User()

@mod.route("/api/v2/auth/signup", methods = ["POST"])
@jwt_required
def create_attendant():
    """
    This endpoint is user by the admin to create an attendant
    """
    role = get_jwt_identity()["user_role"]
    if role != "admin":
        return json_mesages("Access denied","Ask your administrator the right to access these resources")
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

@mod.route("/api/v2/auth/login", methods = ["POST"])
def login():
    """
    TThis endpoint is used by the user to login
    """
    try:
        json.loads(request.get_data())
    except (ValueError, TypeError):
        return json_mesages("Bad request, your request should be in a dictionary format"), 400
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
            usr = fetch_user(data["username"])
            access_token = create_access_token(identity=usr, expires_delta=datetime.timedelta(days=1))
            return jsonify({
                "token": access_token,
                "message": "User successfully login"
            }), 200
        return json_er("Wrong password. Please try again"), 401
    return json_er("User with name {} does not have an account. Please ask your admin to create one"), 401

@mod.route("/api/v2/users/<id>", methods = ["PUT"])
@jwt_required
def update_user_role(id):
    try:
        id = int(id)
    except(ValueError, TypeError):
        return json_er("Bad request. Id should be an integer"), 405
    if valid_id(id) != "Valid":
        return json_er("Invalid Id. Must be a positive number"), 400
    try:
        json.loads(request.get_data())
    except (ValueError, TypeError):
        return json_er("Bad request, your request should be a dictionary"), 400
    data = request.get_json(force=True)
    if not data:
        return json_er("Bad request, your request should be a dictionary"), 400
    if len(data) < 1:
        return json_er("Insuficiant number of inputs. make sure all the fields are inluded"),400
    if len(data) > 1:
        return json_er("Too many arguments. Only user_role is required"), 414
    if not "user_role" in data:
        return json_er("Pease make sure user_role in the request. Check spelling"), 400
    if is_valid_role(data["user_role"]) != "Valid":
        return json_er(is_valid_role(data["user_role"]))
    updated = user.update_user_role(id, data["user_role"])
    updated_user = single_usr(id)
    return json_msg(updated, "User", updated_user), 202
    

@mod.route("/api/v2/products", methods = ["GET"])
@jwt_required
def get_products():
    """
    This endpoint allows the user to fetch all products
    """
    if is_products_empty():
        return json_ms("Oops! There are no products added yet"), 200
    return json_mesages("Products", product.get_all_products()), 200

@mod.route("/api/v2/products", methods = ["POST"])
@jwt_required
def create_product():
    """
    This endpoint is allows the admin to add a new product to the store
    """
    role = get_jwt_identity()["user_role"]
    if role != "admin":
        return json_mesages("Access denied","You have nono right to ")
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

@mod.route("/api/v2/products/<id>", methods = ["PUT"])
@jwt_required
def update_a_product(id):
    """
    This endpoint is allows the admin to update a new product given the product id
    """
    role = get_jwt_identity()["user_role"]
    if role != "admin":
        return json_mesages("Access denied","Ask your administrator the right to access these resources")
    try:
        id = int(id)
    except(ValueError, TypeError):
        return json_er("Bad request. Id should be an integer"), 405
    if valid_id(id) != "Valid":
        return json_er("Invalid Id. Id Must be a positive number"), 400
    try:
        json.loads(request.get_data())
    except (ValueError, TypeError):
        return json_er("Bad request, your request should be a dictionary"), 400
    data = request.get_json(force=True)
    if not data:
        return json_er("Bad request, your request should be a dictionary"), 400
    if len(data) < 4:
        return json_er("Insuficiant number of inputs. make sure all the fields are inluded"),400
    if len(data) > 4:
        return json_er("Too many arguments. Only name, price, quantity, quantity_allowed, and category are required"), 414
    if not "product_name" in data or not "price" in data or not "quantity" in data or not "min_qty_allowed" in data:
        return json_er("Pease make sure name, price, quantity, quantity_allowed are in the request"), 400
    prod_validation = product_update_validation(id, data["product_name"],data["price"],data["quantity"], data["min_qty_allowed"])
    if prod_validation != "Valid":
        return json_er(prod_validation), 417
    prod = product.update_product(id,data["product_name"],data["price"],data["quantity"], data["min_qty_allowed"])
    product_added = single_product_by_id(id)
    return json_msg(prod, "Product", product_added), 202

@mod.route("/api/v2/products/<id>", methods = ["GET"])
@jwt_required
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
    return json_mesages("Product",product.get_product(id)), 200

@mod.route("/api/v2/products/<id>", methods = ["DELETE"])
@jwt_required
def delete_product(id):
    """
    This  endpoint allows the admin to delete a product given the product ID
    """
    role = get_jwt_identity()["user_role"]
    if role != "admin":
        return json_mesages("Access denied","Ask your administrator the right to access these resources")
    try:
        id = int(id)
    except(ValueError, TypeError):
        return json_er("Bad request. Id should be an integer"), 405
    if valid_id(id) != "Valid":
        return json_er("Invalid Id. Must be a positive number"), 400
    product_validation = get_product_id_validation(id)
    if product_validation != "Valid":
        return json_er(product_validation), 404
    deleted_product = single_product_by_id(id)
    delete = product.delete_product(id)
    return json_msg(delete, "Product", deleted_product)

@mod.route("/api/v2/sales", methods = ["POST"])
@jwt_required
def create_sale_order():
    """
    This endpoint allows the store attendant to create a sale record
    """
    role = get_jwt_identity()["user_role"]
    if role != "attendant":
        return json_mesages("Access denied","You have no rights to access these resources"), 409
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

@mod.route("/api/v2/sales", methods = ["GET"])
@jwt_required
def get_all_sales():
    """
    This enpoint allows the owner/admin to view all sales records available
    """
    role = get_jwt_identity()["user_role"]
    if role != "admin":
        return json_mesages("Access denied","Ask your administrator the right to access these resources")
    if is_sales_empty():
        return json_ms("Oh oh! It looks like there is are no sale orders made yet"), 200
    return json_mesages("Sales", sale.get_all_sales()), 200

@mod.route("/api/v2/sales/<id>", methods = ["GET"])
@jwt_required
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
