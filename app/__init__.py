from flask import Flask
from flask_restx import Api
from app.utils.config import Config


app = Flask(__name__)
app.secret_key = 'some_key'
api = Api(app,
          title="Films API",
          description="Here you can get information about thousands"
                      " of movies.",
          default="Film operations",
          default_label="Films related operations",
          doc="/doc/")

app.config.from_object(Config)
