from flask import Blueprint, request, json
from api.validation import json_msg
from api.models import Products, SaleOrder


mod = Blueprint("api", __name__)
product = Products()
sale = SaleOrder()

@mod.route("/products", methods = ["GET"])
def get_products():
    """
    This endpoint allows the user to fetch all products
    """
    return json_msg(product.get_all_products()), 200

@mod.route("/products", methods = ["POST"])
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
        return json_msg("Insuficiant number of inputs. PLz make sure name, price, qty, qty_allowed, and category are included in the request"),400
    if len(data) > 5:
        return json_msg("Too many arguments. Only name, price, qty, qty_allowed, and category are required"), 414
    if not "name" in data or not "price" in data or not "quantity" in data or not "min_quantity" in data or not "category" in data:
        return json_msg("PLz make sure name, price, qty, qty_allowed, and category are included in the request"), 400
    prod = product.add_product(data["name"],data["price"],data["quantity"], data["min_quantity"], data["category"])
    if prod != "Successfully added product":
        return json_msg(prod),417
    return json_msg(prod), 201

    


