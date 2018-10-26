from flask import Blueprint, request, json
from api.validation import valid_id, json_msg
from api.models import Products, SaleOrder


mod = Blueprint("api", __name__)
product = Products()
sale = SaleOrder()

@mod.route("/api/v1/products", methods = ["GET"])
def get_products():
    """
    This endpoint allows the user to fetch all products
    """
    return json_msg(product.get_all_products()), 200

@mod.route("/api/v1/products", methods = ["POST"])
def create_product():
    """
    This endpoint is allows the admin to add a new product to the store
    """
    try:
        json.loads(request.get_data())
    except (ValueError, TypeError):
        return json_msg("Bad request, your request should be a dictionary"), 400
    data = request.get_json(force=True)
    if not data:
        return json_msg("Bad request, your request should be a dictionary"), 400
    if len(data) < 5:
        return json_msg("Insuficiant number of inputs. make sure all the fields are inluded"),400
    if len(data) > 5:
        return json_msg("Too many arguments. Only name, price, quantity, quantity_allowed, and category are required"), 414
    if not "name" in data or not "price" in data or not "quantity" in data or not "min_quantity" in data or not "category" in data:
        return json_msg("Pease make sure name, price, quantity, quantity_allowed, and category are in the request"), 400
    prod = product.add_product(data["name"],data["price"],data["quantity"], data["min_quantity"], data["category"])
    if prod != "Successfully added product":
        return json_msg(prod), 417
    return json_msg(prod), 201

@mod.route("/api/v1/products/<id>", methods = ["GET"])
def get_product(id):
    """
    This endpoint allows the user fetch a specific product
    """
    try:
        id = int(id)
    except(ValueError, TypeError):
        return json_msg("Bad request. Id should be an integer"), 405
    if valid_id(id) != "Valid":
        return json_msg("Invalid Id. Must be a positive number"), 400
    prod = product.get_product(id)
    if not isinstance(prod, dict):
        return json_msg(prod), 404
    return json_msg(prod), 200

@mod.route("/api/v1/sales", methods = ["POST"])
def create_sale_order():
    """
    This endpoint allows the store attendant to create a sale record
    """
    try:
        json.loads(request.get_data())
    except (ValueError, TypeError):
        return json_msg("Bad request, your request should be a dictionary"), 400
    data = request.get_json(force=True)
    if not data:
        return json_msg("Bad request, your request should be a dictionary"), 400
    if len(data) < 3:
        return json_msg("Insuficiant number of inputs. please make sure all the fields are included"), 400
    if len(data) > 3:
        return json_msg("Too many arguments. only product_id, quantity and attendant_name are required"), 414
    if not "product_id" in data or not "quantity" in data or not "at_name" in data: 
        return json_msg("Please make sure product_id, quantity and attendant_name are included int he request")
    order = sale.add_sale_order(data["product_id"], data["quantity"], data["at_name"])
    if order != "Successfully added sale order":
        return json_msg(order), 417
    return json_msg(order), 201

@mod.route("/api/v1/sales", methods = ["GET"])
def get_all_sales():
    """
    This enpoint allows the owner/admin to view all sales records available
    """
    return json_msg(sale.get_all_sales()), 200

@mod.route("/api/v1/sales/<id>", methods = ["GET"])
def get_sale(id):
    """
    This endpoint allows the user to fetch a specific sale record
    """
    try:
        id = int(id)
    except(ValueError, TypeError):
        return json_msg("Invalid request. The Id must be an integer"), 405
    if valid_id(id) != "Valid":
        return json_msg(valid_id(id)), 400
    order = sale.get_sale_record(id)
    if not isinstance(order, dict):
        return json_msg(order), 404
    return json_msg(order), 200
