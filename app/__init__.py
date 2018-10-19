import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from app.api import *
from flask import Flask
from api.views import mod


app = Flask(__name__)
app.register_blueprint(mod)