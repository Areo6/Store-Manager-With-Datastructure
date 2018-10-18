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
    return json_msg("Message", product.get_all_products()), 200

# @mod.route("/products", methods = ["GET"])
# def create_product()
