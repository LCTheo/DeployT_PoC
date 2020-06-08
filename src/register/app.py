from flask import Flask
from flask_restx import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app=app, version='1.0', title='register service', validate=True)


@api.route("/status")
class ResourcesList(Resource):

    def get(self):
        return {'response': "register : online"}, 200
