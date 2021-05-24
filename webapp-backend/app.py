from flask import Flask
from flask_restful import Api

from database.db import initialize_db
from resources.routes import initialize_routes
from resources.errors import errors

app = Flask(__name__)
api = Api(app, errors=errors)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://apkjlezxinqwvu:1de60ac67c90127aeb5e86ee85745c573a3cce9a466ef98cb7d52ce0064432c1@ec2-54-216-185-51.eu-west-1.compute.amazonaws.com:5432/djmradro13nfi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['AUTOCRUD_METADATA_ENABLED'] = True

initialize_db(app)
initialize_routes(api)

app.run(debug=True)
