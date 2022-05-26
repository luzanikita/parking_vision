import os

from flask import Flask
from flask_restful import Api
from libs.flask_restless import APIManager
from flask_cors import CORS

from database.models import MODELS
from database.db import initialize_db, db
from resources.routes import initialize_routes
from resources.errors import errors


app = Flask(__name__)
api = Api(app, errors=errors)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['AUTOCRUD_METADATA_ENABLED'] = True
app.config['CORS_HEADERS'] = 'Content-Type'

initialize_db(app)
initialize_routes(api)

with app.app_context():
    manager = APIManager(app, flask_sqlalchemy_db=db)

    for model in MODELS:
        manager.create_api(model, methods=["GET", "POST", "DELETE", "PUT"])

app.run(host="0.0.0.0", port=5000)
