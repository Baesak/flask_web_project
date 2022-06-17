from flask import Flask
from flask_restx import Api
from app.utils.config import Config


app = Flask(__name__)
app.secret_key = 'some_key'
api = Api(app)

app.config.from_object(Config)
