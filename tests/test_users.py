from flask import json, jsonify
from app import app
import unittest
from database.db import Database


db = Database()


class TestUser(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        db.create_tables()
        db.create_admin()
    
    def tearDown(self):
        db.delete_tables()

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

    def test_if_admin_can_login_successfully(self):
        user = {"username": "malaba", "password": "malaba"}
        response = self.app.post("/api/v2/auth/login", content_type = "json/application", data=json.dumps(user))
        self.assertIn("User successfully login", str(response.data))
        response = self.app.post("/api/v2/auth/login", content_type = "json/application", data=json.dumps({"username": "ma", "password": "malaba"}))
        self.assertIn("Invalid Name. Name must be at least 3 characters", str(response.data))
        
    
    def test_if_admin_can_register_successfully(self):
        token = self.admin_token()
        response = self.app.post('/api/v2/auth/signup', headers={'Authorization': 'Bearer '+ token['token']}, content_type = 'json/application', data=json.dumps({
            "username": "eric",
            "email": "eric@store.com",
            "password": "eubule",
            "user_role": "attendant"
        }))
        self.assertIn("Successfully Created Attendant", str(response.data))
        response = self.app.post("/api/v2/auth/login", content_type = 'json/application', data = json.dumps({'username': 'eric', 'password': 'eubulus'}))
        self.assertIn("Wrong password. Please try again", str(response.data))
        response = self.app.post("/api/v2/auth/login", content_type = 'json/application', data = json.dumps({'username': 'Rick', 'password': 'eubulus'}))
        self.assertIn("User with name Rick does not have an account", str(response.data))
        response = self.app.post("/api/v2/auth/login", content_type = 'json/application', data = json.dumps({'username': 'eric', 'password': 'er'}))
        self.assertEqual(response.status_code, 417)
        response = self.app.post("/api/v2/auth/login", content_type = 'json/application', data = json.dumps({'username': 'eric', 'Oassword': 'eubule'}))
        self.assertEqual(response.status_code, 400)
        response = self.app.post("/api/v2/auth/login", content_type = 'json/application', data = json.dumps({'username': 'eric', 'password': 'eubule', 'other': 'eubule'}))
        self.assertEqual(response.status_code, 414)
        response = self.app.post("/api/v2/auth/login", content_type = 'json/application', data = json.dumps({'username': 'eric'}))
        self.assertEqual(response.status_code, 400)


    def test_if_admin_tries_to_create_user_with_wrong_data(self):
        token = self.attendant_token()
        response = self.app.post('/api/v2/auth/signup', headers={'Authorization': 'Bearer '+ token['token']}, content_type = 'json/application', data=json.dumps({"username": "eric", "email": "eric@store.com", "password": "eubule","user_role": "attendant"}))
        self.assertEqual(response.status_code, 403)
        token = self.admin_token()
        response = self.app.post('/api/v2/auth/signup', headers={'Authorization': 'Bearer '+ token['token']}, content_type = 'json/application', data=json.dumps([]))
        self.assertEqual(response.status_code, 400)
        response = self.app.post('/api/v2/auth/signup', headers={'Authorization': 'Bearer '+ token['token']}, content_type = 'json/application', data=json.dumps({"username": "eric", "email": "eric@store.com", "password": "eubule"}))
        self.assertIn("Missing fields. Please make sure username, email and password are provided", str(response.data))
        response = self.app.post('/api/v2/auth/signup', headers={'Authorization': 'Bearer '+ token['token']}, content_type = 'json/application', data=json.dumps({"username": "eric", "email": "eric@store.com", "password": "eubule","user_role": "attendant", "other": 1}))
        self.assertIn("Too many arguments. Only username, email and password are required", str(response.data))
        response = self.app.post('/api/v2/auth/signup', headers={'Authorization': 'Bearer '+ token['token']}, content_type = 'json/application', data=json.dumps({"username": "eric", "email": "eric@store.com", "password": "eubule","user_rol": "attendant"}))
        self.assertIn("Either username, email, password or user_role is missing. Please check the spelling", str(response.data))
        response = self.app.post('/api/v2/auth/signup', headers={'Authorization': 'Bearer '+ token['token']}, content_type = 'json/application', data=json.dumps({"username": "er", "email": "eric@store.com", "password": "eubule","user_role": "attendant"}))
        self.assertEqual(response.status_code, 417)
        response = self.app.post('/api/v2/auth/signup', headers={'Authorization': 'Bearer '+ token['token']}, content_type = 'json/application', data=json.dumps({"username": "eric", "email": "ericstorecom", "password": "eubule","user_role": "attendant"}))
        self.assertEqual(response.status_code, 417)
        response = self.app.post('/api/v2/auth/signup', headers={'Authorization': 'Bearer '+ token['token']}, content_type = 'json/application', data=json.dumps({"username": "eric", "email": "eric@store.com", "password": "eub","user_role": "attendant"}))
        self.assertEqual(response.status_code, 417)
        response = self.app.post('/api/v2/auth/signup', headers={'Authorization': 'Bearer '+ token['token']}, content_type = 'json/application', data=json.dumps({"username": "eric", "email": "eric@store.com", "password": "eubule","user_role": "atendant"}))
        self.assertEqual(response.status_code, 417)

    def test_if_the_admin_can_successfuly_update_user_role(self):
        token = self.admin_token()
        response = self.app.post('/api/v2/auth/signup', headers={'Authorization': 'Bearer '+ token['token']}, content_type = 'json/application', data=json.dumps({
            "username": "eric",
            "email": "eric@store.com",
            "password": "eubule",
            "user_role": "attendant"
        }))
        response = self.app.put("/api/v2/users/1", headers={'Authorization': 'Bearer '+ token['token']}, content_type = 'json/application', data=json.dumps({"user_role": "admin"}))
        self.assertIn("Successfully updated user role", str(response.data))
    
    def test_if_admin_tries_to_update_user_role_with_wrong_data(self):
        token = self.admin_token()
        response = self.app.put("/api/v2/users/1", headers={'Authorization': 'Bearer '+ token['token']}, content_type = 'json/application', data=json.dumps({"user_role": "admi"}))
        self.assertEqual(response.status_code, 417)
        response = self.app.put("/api/v2/users/1", headers={'Authorization': 'Bearer '+ token['token']}, content_type = 'json/application', data=json.dumps({"user_role": "admin", "other": 1}))
        self.assertIn("Too many arguments. Only user_role is required", str(response.data))
        response = self.app.put("/api/v2/users/1", headers={'Authorization': 'Bearer '+ token['token']}, content_type = 'json/application', data=json.dumps({"user_rolE": "admin"}))
        self.assertIn("Pease make sure user_role in the request. Check spelling", str(response.data))
        response = self.app.put("/api/v2/users/one", headers={'Authorization': 'Bearer '+ token['token']}, content_type = 'json/application', data=json.dumps({"user_role": "admin"}))
        self.assertIn("Bad request. Id should be an integer", str(response.data))
        response = self.app.put("/api/v2/users/0", headers={'Authorization': 'Bearer '+ token['token']}, content_type = 'json/application', data=json.dumps({"user_role": "admin"}))
        self.assertIn("Invalid Id. Must be a positive number", str(response.data))
        response = self.app.put("/api/v2/users/0", headers={'Authorization': 'Bearer '+ token['token']}, content_type = 'json/application', data=json.dumps({}))
        self.assertEqual(response.status_code, 400)
        token = self.attendant_token()
        response = self.app.put("/api/v2/users/0", headers={'Authorization': 'Bearer '+ token['token']}, content_type = 'json/application', data=json.dumps({"user_role": "admin"}))
        self.assertIn("Access denied", str(response.data))

