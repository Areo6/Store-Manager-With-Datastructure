import unittest
from app import app
from api.views import *
from flask import json


class TestProducts(unittest.TestCase):
    """
    This class is meant to test all trafics on products
    """
    def setUp(self):
        """
        This method initializes the flask test client that's gonna help us test endpoints on a no-live server
        """
        self.app = app.test_client()

    def test_return_msg_if_user_try_to_fetch_all_products_when_store_is_empty(self):
        """
        This method tests right message is returned when user tries to access an empty store
        """
        response = self.app.get("/products")
        self.assertEqual(response.status_code, 200)
    
    def test_return_msg_if_user_try_to_fetch_a_specific_product_not_found_in_store(self):
        """
        This method tests right message is returned when user tries to fetch a specific product that's not found in store
        """
        response = self.app.get("products/6")
        self.assertEqual(response.status_code, 404)
        response = self.app.get("products/0")
        self.assertEqual(response.status_code, 400)

    def test_if_admin_try_to_add_product_with_wrong_data(self):
        """
        This method tests if error message is returned when admin tries to add product with wrong data 
        """
        response = self.app.post("/products", content_type = "application/json", data = json.dumps({
            "name": "LD", "price": 400000, "quantity": 45,"min_quantity": 1, "category": "TVs"
        }))
        self.assertEqual(response.status_code, 417)
        response = self.app.post("/products", content_type = "application/json", data = json.dumps({
            "name": "LD1", "price": 400000, "quantity": 45,"min_quantity": 1, "category": "Ca"
        }))
        self.assertEqual(response.status_code, 417)
        response = self.app.post("/products", content_type = "application/json", data = json.dumps({
            "name": "LD1", "price": 400000, "quantity": 45,"min_quantity": 46, "category": "TVs"
        }))
        self.assertEqual(response.status_code, 417)
        response = self.app.post("/products", content_type = "application/json", data = json.dumps({
            "name": "LD1", "price": 400000, "quantity": 45,"min_quantity": 1, "category": 1
        }))
        self.assertEqual(response.status_code, 417)
        response = self.app.post("/products", content_type = "application/json", data = json.dumps({
            "name": "LD1", "price": "me", "quantity": 45,"min_quantity": 1, "category": "TVs"
        }))
        self.assertEqual(response.status_code, 417)
        response = self.app.post("/products", content_type = "application/json", data = json.dumps({
            "name": 1, "price": 440000, "quantity": 45,"min_quantity": 1, "category": "TVs"
        }))
        self.assertEqual(response.status_code, 417)
        response = self.app.post("/products", content_type = "application/json", data = json.dumps({
            "name": "LD1", "price": -450000, "quantity": 45,"min_quantity": 1, "category": "TVs"
        }))
        self.assertEqual(response.status_code, 417)
        response = self.app.post("/products", content_type = "application/json", data = json.dumps({
            "name": "LD1", "price": 450000, "quantity": 45,"min_quantity": 1, "category": ""
        }))
        self.assertEqual(response.status_code, 417)
    
    def test_if_admin_tries_to_add_product_with_mising_or_more_fields(self):
        """
        This method tests if the admin tries to add a product with missing or more field
        """
        response = self.app.post("/products", content_type = "application/json", data = json.dumps({
            "name": "LD1", "quantity": 45,"min_quantity": 1, "category": "TVs"
        }))
        self.assertIn("Insuficiant number of inputs. PLz make sure name, price, qty, qty_allowed, and category are included in the request", str(response.data))
        response = self.app.post("/products", content_type = "application/json", data = json.dumps({
            "name": "LD1", "price": 400000, "quantity": 45,"min_quantity": 1, "category": "TVs", "other": 2
        }))
        self.assertEqual(response.status_code, 414)

    def test_if_user_tries_to_add_product_with_no_data(self):
        """
        This method tests if response returned is an error when user tried to add product with no data provided
        """
        response = self.app.post("/products", content_type = "application/json", data = None)
        self.assertIn("Bad request, your request should be a dictionary", str(response.data))
        response = self.app.post("/products", content_type = "application/json", data = json.dumps({}))
        self.assertIn("Bad request, your request should be a dictionary", str(response.data))
    
    def test_if_admin_adds_product_successfully(self):
        """
        This method tests if the the admin can successfully add a new product to the store
        """
        response = self.app.post("/products", content_type = "application/json", data = json.dumps({
            "name": "LD1", "price": 400000, "quantity": 45,"min_quantity": 1, "category": "TVs"
        }))
        self.assertEqual(response.status_code, 201)
        response = self.app.post("/products", content_type = "application/json", data = json.dumps({
            "name": "LD1", "price": 400000, "quantity": 45,"min_quantity": 1, "category": "TVs"
        }))
        self.assertEqual(response.status_code, 417)

    def test_if_user_can_successfully_fetch_all_products(self):
        """
        This method tests if user can successfully fecth all products
        """
        response = self.app.get("/products")
        self.assertEqual(response.status_code, 200)
    
    def test_if_user_can_successfully_fetch_a_specific_product(self):
        """
        This method tests if user can successfully fecth a specific product
        """
        response = self.app.get("/products/1")
        self.assertEqual(response.status_code, 200)