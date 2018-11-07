from flask import json, jsonify
from app import app
import unittest
from api.db import Database


db = Database()


class TestProduct(unittest.TestCase):

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

    def test_if_admin_can_successfully_add_product(self):
        token = self.admin_token()
        product = {"product_name": "DVD1", "price": 150000, "quantity": 43, "min_qty_allowed": 1}
        response = self.app.post("/api/v2/products", content_type = "json/application",headers = {'Authorization' : 'Bearer '+ token['token']}, data=json.dumps(product))
        self.assertIn("Successfully Added Product", str(response.data))

    def test_if_admin_tries_add_product_with_mising_field(self):
        token = self.admin_token()
        product = {"product_name": "DVD1", "price": 150000, "quantity": 43}
        response = self.app.post("/api/v2/products", content_type='json/application', headers = {'Authorization': 'Bearer ' + token['token']}, data = json.dumps(product))
        self.assertIn("Insuficiant number of inputs. make sure all the fields are inluded", str(response.data))
        response = self.app.post("/api/v2/products", content_type='json/application', headers = {'Authorization': 'Bearer ' + token['token']}, data = json.dumps({"product_name": "DVD1", "price": 150000, "quantity": 43, "min_qty_allowed": 1, "other": 2}))
        self.assertIn("Too many arguments. Only name, price, quantity, quantity_allowed, and category are required", str(response.data))
        response = self.app.post("/api/v2/products", content_type='json/application', headers = {'Authorization': 'Bearer ' + token['token']}, data = json.dumps({"product_name": "DVD1", "price": 150000, "quantity": 43, "min_qty_allowe": 1}))
        self.assertIn("Please make sure name, price, quantity, quantity_allowed are in the request", str(response.data))
        response = self.app.post("/api/v2/products", content_type='json/application', headers = {'Authorization': 'Bearer ' + token['token']}, data = json.dumps([]))
        self.assertEqual(response.status_code, 400)


    def test_if_user_tries_add_product_with_invalid_data(self):
        token = self.admin_token()
        product = {"product_name": "DV", "price": 150000, "quantity": 43, "min_qty_alowed": 1}
        response = self.app.post("/api/v2/products", content_type = "json/application", headers = {'Authorization': 'Bearer ' + token['token']}, data = json.dumps({"product_name": "DV", "price": 150000, "quantity": 43, "min_qty_allowed": 1}))
        self.assertEqual(response.status_code, 417)
        product = {"product_name": "DVD", "price": 150000, "quantity": 0, "min_qty_allowed": 1}
        response = self.app.post("/api/v2/products", content_type= "json/application", headers = {'Authorization': 'Bearer ' + token['token']}, data = json.dumps(product))
        self.assertEqual(response.status_code, 417)
        product = {"product_name": "DVD", "price": 0, "quantity": 1, "min_qty_allowed": 1}
        response = self.app.post("/api/v2/products", content_type= "json/application", headers = {'Authorization': 'Bearer ' + token['token']}, data = json.dumps(product))
        self.assertEqual(response.status_code, 417)
        product = {"product_name": "DVD", "price": 300000, "quantity": 1, "min_qty_allowed": -1}
        response = self.app.post("/api/v2/products", content_type= "json/application", headers = {'Authorization': 'Bearer ' + token['token']}, data = json.dumps(product))
        self.assertEqual(response.status_code, 417)
    
    def test_if_attendant_tries_to_create_a_product(self):
        token = self.attendant_token()
        response = self.app.post("/api/v2/products", content_type = "json/application", headers = {'Authorization': 'Bearer ' + token['token']}, data = json.dumps({"product_name": "DVD", "price": 150000, "quantity": 43, "min_qty_allowed": 1}))
        self.assertIn("You have no right to access this resource", str(response.data))

    def test_if_admin_can_update_a_product(self):
        token = self.admin_token()
        product = {"product_name": "DVD1", "price": 150000, "quantity": 43, "min_qty_allowed": 1}
        response = self.app.post("/api/v2/products", content_type = "json/application",headers = {'Authorization' : 'Bearer '+ token['token']}, data=json.dumps(product))
        response = self.app.put("/api/v2/products/1", content_type = "json/application", headers = {'Authorization': 'Bearer ' + token['token']}, data = json.dumps({"product_name": "DVD2", "price": 300000, "quantity": 43, "min_qty_allowed": 1}))
        self.assertEqual(response.status_code, 202)  

    def test_if_user_can_view_all_products(self):
        token = self.attendant_token()
        response = self.app.get("/api/v2/products", headers = {'Authorization' : 'Bearer ' + token ['token']})
        self.assertIn("Oops! There are no products added yet", str(response.data))
        token = self.admin_token()
        product = {"product_name": "DVD1", "price": 150000, "quantity": 43, "min_qty_allowed": 1}
        response = self.app.post("/api/v2/products", content_type = "json/application",headers = {'Authorization' : 'Bearer '+ token['token']}, data=json.dumps(product))
        token = self.attendant_token()
        response = self.app.get("/api/v2/products", headers = {'Authorization' : 'Bearer ' + token ['token']})
        self.assertIn("Product", str(response.data))
       
    def test_if_user_can_fetch_a_specific_product(self):
        token = self.admin_token()
        product = {"product_name": "DVD3", "price": 150000, "quantity": 43, "min_qty_allowed": 1}
        response = self.app.post("/api/v2/products", content_type = "json/application",headers = {'Authorization' : 'Bearer '+ token['token']}, data=json.dumps(product))
        token = self.attendant_token()
        response = self.app.get("/api/v2/products/1", headers = {'Authorization' : 'Bearer ' + token['token']})
        self.assertIn("Product",str(response.data))
    
    def test_if_user_tries_to_fetch_an_non_existat_product(self):
        token = self.admin_token()
        product = {"product_name": "DVD3", "price": 150000, "quantity": 43, "min_qty_allowed": 1}
        response = self.app.post("/api/v2/products", content_type = "json/application",headers = {'Authorization' : 'Bearer '+ token['token']}, data=json.dumps(product))
        token = self.attendant_token()
        response = self.app.get("/api/v2/products/4", headers = {'Authorization' : 'Bearer ' + token['token']})
        self.assertEqual(response.status_code, 404)

    def test_if_admin_provides_a_non_integer_to_fetch_a_product(self):
        token = self.admin_token()
        response = self.app.get("/api/v2/products/m", headers = {'Authorization' : 'Bearer ' + token['token']})
        self.assertIn("Bad request. Id should be an integer", str(response.data))

    def test_if_admin_can_delete_a_product(self):
        token = self.admin_token()
        response = self.app.post("/api/v2/products", content_type='application/json', headers = {'Authorization' : 'Bearer ' + token['token']}, data = json.dumps({"product_name": "DVD3", "price": 150000, "quantity": 43, "min_qty_allowed": 1}))
        response = self.app.delete("/api/v2/products/one", headers = {'Authorization' : 'Bearer ' + token['token']})
        self.assertEqual(response.status_code, 405)
        response = self.app.delete("/api/v2/products/0", headers = {'Authorization' : 'Bearer ' + token['token']})
        self.assertEqual(response.status_code, 400)
        response = self.app.delete("/api/v2/products/2", headers = {'Authorization' : 'Bearer ' + token['token']})
        self.assertEqual(response.status_code, 404)
        response = self.app.delete("/api/v2/products/1", headers = {'Authorization' : 'Bearer ' + token['token']})
        self.assertIn("Successfully deleted product", str(response.data))