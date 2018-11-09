from flask import Flask
from app.api.views import mod
from flask_jwt_extended import JWTManager
from Instance.config import DevelopmentConfig


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config['JWT_SECRET_KEY']  = 'hard-to-guess'
app.register_blueprint(mod)
jwt = JWTManager(app)