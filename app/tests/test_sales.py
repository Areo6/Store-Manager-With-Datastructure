import unittest
from app import app
from api.views import *
from flask import json


class TestSales(unittest.TestCase):
    """
    This class is used test all trafics on products
    """
    def setUp(self):
        """
        This method initializes the flask test client that's gonna help us test endpoints on a no-live server
        """
        self.app = app.test_client()

    def test_return_msg_if_user_try_to_fetch_all_sale_records_when_empty(self):
        """
        This method tests right message is returned when the admin tries to fetch empty sale record
        """
        response = self.app.get("/sales")
        self.assertEqual(response.status_code, 200)
    
    def test_return_msg_if_user_try_to_fetch_a_specific_sale_record_that_does_not_exist(self):
        """
        This method tests right message is returned when user tries to fetch a specific  sale record that does not exist
        """
        response = self.app.get("sales/6")
        self.assertEqual(response.status_code, 404)
        response = self.app.get("sales/0")
        self.assertEqual(response.status_code, 400)

    def test_if_attendant_try_to_add_sale_record_with_wrong_data(self):
        """
        This method tests if error message is returned when admin tries to add product with wrong data 
        """
        response = self.app.post("/sales", content_type = "application/json", data = json.dumps({
            "product_id": 0, "quantity": 1, "at_name": "Eric"
        }))
        self.assertEqual(response.status_code, 417)
        response = self.app.post("/sales", content_type = "application/json", data = json.dumps({
            "product_id": "me", "quantity": 1, "at_name": "Eric"
        }))
        self.assertEqual(response.status_code, 417)
        response = self.app.post("/sales", content_type = "application/json", data = json.dumps({
            "product_id": 1, "quantity": -9, "at_name": "Eric"
        }))
        self.assertIn("Invalid quantity. Qty must be greater than 0",str(response.data))
        response = self.app.post("/sales", content_type = "application/json", data = json.dumps({
            "product_id": 1, "quantity": 1, "at_name": "Er"
        }))
        self.assertEqual(response.status_code, 417)
        response = self.app.post("/sales", content_type = "application/json", data = json.dumps({
            "product_id": 1, "quantity": 50, "at_name": "Eric"
        }))
        self.assertEqual(response.status_code, 417)
        response = self.app.post("/sales", content_type = "application/json", data = json.dumps({
            "product_id": 1, "quantity": "three", "at_name": "Eric"
        }))
        self.assertEqual(response.status_code, 417)
    
    def test_if_user_tries_to_add_sale_record_with_mising_or_more_fields(self):
        """
        This method tests if the attendant tries to add a sale record with missing or more field
        """
        response = self.app.post("/sales", content_type = "application/json", data = json.dumps({
            "product_id": 1, "quantity": 1
        }))
        self.assertIn("Insuficiant number of inputs. PLz make sure product_id, quantity and attendant_name are included in the request", str(response.data))
        response = self.app.post("/sales", content_type = "application/json", data = json.dumps({
            "product_id": 1, "quantity": 1, "at_name": "Eric", "other": 2
        }))
        self.assertEqual(response.status_code, 414)
    
    def test_if_user_tries_to_add_sale_record_with_no_data(self):
        """
        This method tests if response returned is an error when user tried to add sale record with no data provided
        """
        response = self.app.post("/sales", content_type = "application/json", data = None)
        self.assertIn("Bad request, your request should be a dictionary", str(response.data))
        response = self.app.post("/sales", content_type = "application/json", data = json.dumps({}))
        self.assertIn("Bad request, your request should be a dictionary", str(response.data))
    
    def test_if_attendant_adds_sale_record_successfully(self):
        """
        This method tests if the the store attendant can successfully add a new sale record
        """
        response = self.app.post("/products", content_type = "application/json", data = json.dumps({
            "name": "LD2", "price": 400000, "quantity": 45,"min_quantity": 1, "category": "TVs"
        }))
        response = self.app.post("/sales", content_type = "application/json", data = json.dumps({
            "product_id": 1, "quantity": 1, "at_name": "Eric"
        }))
        self.assertEqual(response.status_code, 201)
    
    def test_if_admin_can_successfully_fetch_all_sale_records(self):
        """
        This method tests if admin can successfully fecth all sale records
        """
        response = self.app.get("/sales")
        self.assertEqual(response.status_code, 200)
    
    def test_if_user_can_successfully_fetch_a_specific_sale_record(self):
        """
        This method tests if user can successfully fecth a specific sale record
        """
        response = self.app.get("/sales/1")
        self.assertEqual(response.status_code, 200)