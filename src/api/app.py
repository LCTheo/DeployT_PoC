import time

from flask import Flask, request, send_file, render_template
from flask_restx import Api, Resource, reqparse, fields
import os
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)
api = Api(app=app, version='0.1', title='DeployT API', validate=True)
user_definition = api.model('User Informations', {
    'login': fields.String(required=True),
    'password': fields.String(required=True)
})
registerAddress = "register"
serviceName = os.getenv('name')
payload = {'type': 'api', 'address': os.getenv('name')}
r = requests.post('http://register:5000/registration', params=payload)
atempt = 1
while r.status_code != 200:
    if atempt == 3:
        app.logger.error('error while api registration')
        exit(1)
    time.sleep(5)
    r = requests.post('http://register:5000/registration', params=payload)
    atempt += 1
app.logger.info('api successfully registered')


@api.route("/api/status")
class status(Resource):

    def get(self):
        response = requests.get('http://register:5000/status')
        return response.json(), 200


@api.route("/api/user/registration")
class user_registration(Resource):

    @api.expect(user_definition)
    def post(self):
        data = request.get_json()
        response = requests.post('http://registration:5000/registration/user', json={'login': data.get('login'),
                                                                                     'password': data.get('password')})
        if response.status_code == 200:
            return response.json(), 200
        else:
            return {}, response.status_code

    @api.expect(user_definition)
    def delete(self):
        data = request.get_json()
        response = requests.delete('http://registration:5000/registration/user', json={'login': data.get('login'),
                                                                                       'password': data.get('password')})
        if response.status_code == 200:
            return response.json(), 200
        else:
            return {}, response.status_code


@api.route("/api/admin/registration")
class admin_registration(Resource):

    @api.expect(user_definition)
    def post(self):
        data = request.get_json()
        response = requests.post('http://registration:5000/registration/admin', json={'login': data.get('login'),
                                                                                      'password': data.get('password')})
        if response.status_code == 200:
            return response.json(), 200
        else:
            return {}, response.status_code

    @api.expect(user_definition)
    def delete(self):
        data = request.get_json()
        response = requests.delete('http://registration:5000/registration/admin', json={'login': data.get('login'),
                                                                                        'password': data.get('password')})
        if response.status_code == 200:
            return response.json(), 200
        else:
            return {}, response.status_code


if __name__ == "__main__":
    app.run(host='0.0.0.0')
