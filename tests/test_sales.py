from flask import json, jsonify
from app import app
import unittest
from database.db import Database


db = Database()


class TestSale(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        db.create_tables()
        db.create_admin()
    
    def admin_token(self):
        response = self.app.post('/api/v2/auth/login', content_type = 'json/application', data=json.dumps(dict(
            username= "malaba",
            password= "malaba"
        ),))
        token = json.loads(response.data)
        return token
    
    def attendant_token(self):
        token = self.admin_token()
        response = self.app.post('/api/v2/auth/signup', headers={'Authorization': 'Bearer '+ token['token']}, content_type = 'json/application', data=json.dumps({
            "username": "eric",
            "email": "eric@store.com",
            "password": "eubule",
            "user_role": "attendant"
        }))
        response = self.app.post('/api/v2/auth/login', content_type = 'json/application', data=json.dumps(dict(
            username= "eric",
            password= "eubule"
        ),))
        token = json.loads(response.data)
        return token
    
    def tearDown(self):
        db.delete_tables()
    
    def test_if_attendant_can_successfuly_make_a_sale_order(self):
        token = self.admin_token()
        product = {"product_name": "DVD1", "price": 150000, "quantity": 43, "min_qty_allowed": 1}
        response = self.app.post("/api/v2/products", content_type = "json/application",headers = {'Authorization' : 'Bearer '+ token['token']}, data=json.dumps(product))
        response = self.app.post("/api/v2/sales", content_type = 'json/application', headers = {'Authorization' : 'Bearer ' + token['token']}, data = json.dumps({"product_id": 1, "quantity": 1, "attendant_name": "Eric"}))
        self.assertEqual(response.status_code, 403)
        token = self.attendant_token()
        response = self.app.post("/api/v2/sales", content_type = 'json/application', headers = {'Authorization' : 'Bearer ' + token['token']}, data = json.dumps({"product_id": 1, "quantity": 1, "attendant_name": "Eric"}))
        self.assertEqual(response.status_code, 201)
    
    def test_if_user_tries_to_make_sale_with_wrong_data(self):
        token = self.admin_token()
        product = {"product_name": "DVD1", "price": 150000, "quantity": 43, "min_qty_allowed": 1}
        response = self.app.post("/api/v2/products", content_type = "json/application",headers = {'Authorization' : 'Bearer '+ token['token']}, data=json.dumps(product))
        token = self.attendant_token()
        response = self.app.post("/api/v2/sales", content_type = 'json/application', headers = {'Authorization' : 'Bearer ' + token['token']}, data = json.dumps({}))
        self.assertIn("Bad request, your request should be a dictionary", str(response.data))
        response = self.app.post("/api/v2/sales", content_type = 'json/application', headers = {'Authorization' : 'Bearer ' + token['token']}, data = json.dumps({"product_id": 1, "attendant_name": "Eric"}))
        self.assertIn("Insuficiant number of inputs. please make sure all the fields are included", str(response.data))
        response = self.app.post("/api/v2/sales", content_type = 'json/application', headers = {'Authorization' : 'Bearer ' + token['token']}, data = json.dumps({"product_id": 1, "quantity": 1, "attendant_name": "Eric", "other": 1}))
        self.assertEqual(response.status_code, 414)
        response = self.app.post("/api/v2/sales", content_type = 'json/application', headers = {'Authorization' : 'Bearer ' + token['token']}, data = json.dumps({"Product_id": 1, "quantity": 1, "attendant_name": "Eric"}))
        self.assertEqual(response.status_code, 400)
        response = self.app.post("/api/v2/sales", content_type = 'json/application', headers = {'Authorization' : 'Bearer ' + token['token']}, data = json.dumps({"product_id": 1, "quantity": -3, "attendant_name": "Eric"}))
        self.assertEqual(response.status_code, 417)
        response = self.app.post("/api/v2/sales", content_type = 'json/application', headers = {'Authorization' : 'Bearer ' + token['token']}, data = json.dumps({"product_id": 4, "quantity": 1, "attendant_name": "Eric"}))
        self.assertIn("Product with id 4 does not exist", str(response.data))
    
    def test_if_admin_tries_to_fetch_sales_when_there_is_no_sales_made_yet(self):
        token = self.attendant_token()
        response = self.app.get("/api/v2/sales", headers = {'Authorization' : 'Bearer ' + token['token']})
        self.assertEqual(response.status_code, 403)
        token = self.admin_token()
        response = self.app.get("/api/v2/sales", headers = {'Authorization' : 'Bearer ' + token['token']})
        self.assertIn("Oh oh! It looks like there is are no sale orders made yet", str(response.data))

    def test_if_admin_can_successfully_fetch_all_products(self):
        token = self.admin_token()
        product = {"product_name": "DVD1", "price": 150000, "quantity": 43, "min_qty_allowed": 1}
        response = self.app.post("/api/v2/products", content_type = "json/application",headers = {'Authorization' : 'Bearer '+ token['token']}, data=json.dumps(product))
        token = self.attendant_token()
        response = self.app.post("/api/v2/sales", content_type = 'json/application', headers = {'Authorization' : 'Bearer ' + token['token']}, data = json.dumps({"product_id": 1, "quantity": 1, "attendant_name": "Eric"}))
        token = self.admin_token()
        response = self.app.get("/api/v2/sales", headers = {'Authorization' : 'Bearer ' + token['token']})
        self.assertIn("Sales", str(response.data))

    def test_if_user_can_successfully_fetch_a_specific_sale_order(self):
        token = self.admin_token()
        product = {"product_name": "DVD1", "price": 150000, "quantity": 43, "min_qty_allowed": 1}
        response = self.app.post("/api/v2/products", content_type = "json/application",headers = {'Authorization' : 'Bearer '+ token['token']}, data=json.dumps(product))
        token = self.attendant_token()
        response = self.app.post("/api/v2/sales", content_type = 'json/application', headers = {'Authorization' : 'Bearer ' + token['token']}, data = json.dumps({"product_id": 1, "quantity": 1, "attendant_name": "Eric"}))
        response = self.app.get("/api/v2/sales/me", headers = {'Authorization' : 'Bearer ' + token['token']})
        self.assertIn("Bad request. Id should be an integer", str(response.data))
        response = self.app.get("/api/v2/sales/0", headers = {'Authorization' : 'Bearer ' + token['token']})
        self.assertIn("Invalid Id. Must be a positive number", str(response.data))
        response = self.app.get("/api/v2/sales/3", headers = {'Authorization' : 'Bearer ' + token['token']})
        self.assertIn("Sale with id 3 not found", str(response.data))
        response = self.app.get("/api/v2/sales/1", headers = {'Authorization' : 'Bearer ' + token['token']})
        self.assertIn("Sale order", str(response.data))