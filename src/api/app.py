import time

from flask import Flask, request, send_file, render_template
from flask_restx import Api, Resource, reqparse
import os
from os import path
from werkzeug.utils import secure_filename
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)
api = Api(app=app, version='0.1', title='DeployT API', validate=True)

registerAddress = "register"
serviceName = os.getenv('name')
payload = {'type': 'api', 'address': os.getenv('name')}
r = requests.post('http://register:5000/registration', params=payload)
atempt = 1
while r.status_code != 200:
    if atempt == 3:
        app.logger.error('error while api registration')
        exit(1)
    time.sleep(1)
    r = requests.post('http://register:5000/registration', params=payload)
    atempt += 1
app.logger.info('api successfully registered')


@api.route("/api/status")
class status(Resource):

    def get(self):
        response = requests.get('http://register:5000/status')
        return {response.json()}, 200


if __name__ == "__main__":
    app.run(host='0.0.0.0')
