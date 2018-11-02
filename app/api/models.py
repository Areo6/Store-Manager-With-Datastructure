from api.validation import *
from api.db import Database


db = Database()
cursor = db.cur


class User():
    """
    This is class creates a new user and is responsible for all user operations

    """

    def create_user(self,username, email, password, user_role):
        """This method adds a new user in the database"""
        query = ("""INSERT INTO users (username, email,password, user_role) VALUES ('{}','{}','{}', '{}')""".format(username, email, password, user_role))
        cursor.execute(query)
        return "Successfully Created Attendant"

    def login(self, username):
        """
        This method allows the user to login 
        """
        query = ("""SELECT * FROM users WHERE username = '{}'""".format(username))
        cursor.execute(query)
        user = cursor.fetchone()
        return user

    def search_user_name(self,username):
        """This method searchs if username exists and returns user records"""
        query = ("""SELECT * FROM users WHERE username = '{}'""".format(username))
        cursor.execute(query)
        user = cursor.fetchone()
        return user
    
    def update_user_role(seld,user_id, user_role):
        """
        This method allows the admin to grant the attend the admin rights
        """
        query = ("""UPDATE users SET (user_role) = ('{}') WHERE user_id = '{}'""".format(user_role, user_id))
        cursor.execute(query)
        return "Successfully updated user role"

class Products():
    """
    This class deals with all the product's manipulations
    """    
    def get_all_products(self):
        """
        This method is used by the admin to view all the products in store
        """
        query = ("""SELECT * FROM products;""" )
        cursor.execute(query)
        products = cursor.fetchall()
        return products
    
    def get_product(self, id):
        """
        This method is used to fetch a specific product given the product's id
        """
        query = ("""SELECT * FROM products WHERE product_id = '{}'""".format(id))
        cursor.execute(query)
        product = cursor.fetchone()
        return product

    def add_product(self, name, price, qty_available, min_qty_allowed):
        """
        This hemethod is used by the admin to add a product in the store
        """
        query = ("""INSERT INTO products (product_name, price, quantity, min_qty_allowed) VALUES('{}', '{}', '{}', '{}')""".format(name, price, qty_available, min_qty_allowed))
        cursor.execute(query)
        return "Successfully Added Product"
    
    def update_product(self,id, product_name, price, qty_available, min_qty_allowed):
        """
        This method allows for updating or editing a product
        """
        query = ("""UPDATE products SET product_name='{}', price='{}', quantity='{}', min_qty_allowed='{}' WHERE product_id = '{}'""".format(product_name,price, qty_available, min_qty_allowed, id))
        cursor.execute(query)
        return "Successfully updated product"

    def delete_product(self, product_id):
        """
        This method allows the the admin user to delete a product given the product name
        """
        query = ("""DELETE FROM products WHERE product_id = '{}'""".format(product_id))
        cursor.execute(query)
        return "Successfully deleted product"


class SaleOrder():
    """
    This class deals with all sale's trafics
    """
    def add_sale_order(self, product_id, quantity, attendant_name):
        """
        This method is used by the store attendant to add a sale order
        """
        query = ("""SELECT price FROM products WHERE product_id = '{}'""".format(product_id))
        cursor.execute(query)
        price = cursor.fetchone()
        price = price["price"]
        total_amount = price * quantity
        query = ("""INSERT INTO sales (product_id, price, quantity, total_amount, attendant_name) VALUES('{}', '{}', '{}', '{}', '{}')""".format(product_id, price, quantity, total_amount, attendant_name))
        cursor.execute(query)
        return "Successfully added sale order"

    def get_all_sales(self):
        """
        This allows the admin user to ftch all the sale order records
        """
        query = ("""SELECT * FROM sales;""" )
        cursor.execute(query)
        sales = cursor.fetchall()
        return sales

    def get_sale_record(self,id):
        """
        This method allows the user to fetch a specif sale record
        """
        query = ("""SELECT * FROM sales WHERE sale_id = '{}'""".format(id))
        cursor.execute(query)
        sale = cursor.fetchone()
        return sale
    