from api.validation import *
from api.db import Database


db = Database()
cursor = db.cur

class Products():
    """
    This class deals with all the product's manipulations
    """
    def is_existing_product(self,product_name):
        """
        This method checks if a product with the given name already exists in the database
        """
        query = ("""SELECT * FROM products WHERE product_name = '{}'""".format(product_name))
        cursor.execute(query)
        product = cursor.fetchone();
        if product:
            return True
        else:
            return False
    
    def get_all_products(self):
        """
        This method is used by the admin to view all the products in store
        """
        query = ("""SELECT * FROM products;""" )
        cursor.execute(query)
        products = cursor.fetchall()
        # if len(Products) == 0:
        #     return "Oops. It's still lonely here. No products yet"
        return products
    
    def get_product(self, id):
        """
        This method is used to fetch a specific product given the product's id
        """
        if valid_id(id) != "Valid":
            return valid_id(id)
        query = ("""SELECT * FROM products WHERE product_id = '{}'""".format(id))
        cursor.execute(query)
        product = cursor.fetchone()
        if not product:
            return "Product with id {} not found. put a valid id".format(id)
        return product

    def add_product(self, name, price, qty_available, min_qty_allowed):
        """
        This hemethod is used by the admin to add a product in the store
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
        query = ("""SELECT product_name FROM products;""")
        cursor.execute(query)
        product = cursor.fetchone()
        if product:
            return "Product with name {} already exists. Choose another name".format(name)
        query = ("""INSERT INTO products (product_name, price, quantity, min_qty_allowed) VALUES('{}', '{}', '{}', '{}')""".format(name, price, qty_available, min_qty_allowed))
        cursor.execute(query)
        return "Successfully added product"

class SaleOrder():
    """
    This class deals with all sale's trafics
    """
    def add_sale_order(self, prod_id, quantity, attendant_name):
        """
        This method is used by the store attendant to add a sale order
        """
        if valid_id(prod_id) != "Valid":
            return valid_id(prod_id)
        if valid_quantity(quantity) != "Valid":
            return valid_quantity(quantity)
        if valid_name(attendant_name) != "Valid":
            return valid_name(attendant_name)
        if len(products) == 0:
            return "Empty store. There are no products in store yet"
        prod = [x for x in products if x["id"] == prod_id]
        if len(prod) == 0:
            return "Product with id {} was not found in store.".format(prod_id)
        qty = prod[0]["quantity"]
        if quantity > qty:
            return "Invalid quantity. Quantity ordered must be less than {}(quantity in store)".format(qty)
        price = prod[0]["price"]
        id = len(sales) + 1
        total = price * quantity
        order = {
            "id": id,
            "product_id": prod_id,
            "price": price,
            "quantity": quantity,
            "total_amount": total,
            "attendant_name": attendant_name
        }
        sales.append(order)
        return "Successfully added sale order"

    def get_all_sales(self):
        """
        This allows the admin user to ftch all the sale order records
        """
        if len(sales) == 0:
            return "Oops! The are no sale orders made yet"
        return sales

    def get_sale_record(self,id):
        """
        This method allows the user to fetch a specif sale record
        """
        if valid_id(id) != "Valid":
            return valid_id(id)
        if len(sales) == 0:
            return "Oops! It's lonely here. No sale records yet"
        order = [x for x in sales if x["id"] == id]
        if len(order) == 0:
            return "Sale record number {} is not found in the sale records".format(id)
        return order[0]
    