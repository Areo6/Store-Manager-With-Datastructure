import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from app.api import *
from flask import Flask
from app.api.views import mod
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config['JWT_SECRET_KEY']  = 'hard-to-guess'
app.register_blueprint(mod)
jwt = JWTManager(app)