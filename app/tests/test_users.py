from flask import json, jsonify
from app import app
import unittest
from app.api.db import Database


db = Database()


class TestUser(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        db.create_tables()
        db.create_admin()
    
    def tearDown(self):
        db.delete_tables()

    def test_if_admin_can_login_successfully(self):
        user = {"username": "malaba", "password": "malaba"}
        response = self.app.post("/api/v2/auth/login", content_type = "json/application", data=json.dumps(user))
        # print(response.data)
        self.assertIn("User successfully login", str(response.data))
        print(response.data)
        
    
    def test_if_admin_can_register_successfully(self):
        response = self.app.post('/api/v2/auth/login', content_type = 'json/application', data=json.dumps(dict(
            username= "malaba",
            password= "malaba"
        ),))
        # print (response.data)
        token = json.loads(response.data)
        response = self.app.post('/api/v2/auth/signup', headers={'Authorization': 'Bearer '+ token['token']}, content_type = 'json/application', data=json.dumps({
            "username": "eric",
            "email": "eric@store.com",
            "password": "eubule",
            "user_role": "attendant"
        }))
        self.assertIn("Successfully Created Attendant", str(response.data))






