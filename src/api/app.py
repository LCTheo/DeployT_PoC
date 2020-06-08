from flask import Flask, request, send_file, render_template
from flask_restx import Api, Resource, reqparse
import os
from os import path
from werkzeug.utils import secure_filename
from flask_cors import CORS
import requests


app = Flask(__name__)
CORS(app)
api = Api(app=app, version='1.0', title='Resources Doc API', validate=True)

registerAddress = "register"


@api.route("/api/status")
class ResourcesList(Resource):

    def get(self):
        r = requests.get('http://register:5000/status')
        return {'response': r.json()}, 200
