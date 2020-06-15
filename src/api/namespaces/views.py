from flask import request
from flask_restx import Namespace, Resource

import requests
from .models import user_definition, delete_model, token_model

api = Namespace('views', description='route of the api', path="/")


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

    @api.expect(delete_model)
    def delete(self):
        data = request.get_json()
        validation = requests.get('http://oauth:5000/validate', json={'token': data.get('token'),
                                                                      'user_id': data.get('user_id')})
        if validation.status_code == 200:
            response = requests.delete('http://registration:5000/registration/user', json={'token': data.get('token')})
            if response.status_code == 200:
                return response.json(), 200
            else:
                return {}, response.status_code
        else:
            return


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
                                                                                        'password': data.get(
                                                                                            'password')})
        if response.status_code == 200:
            return response.json(), 200
        else:
            return {}, response.status_code


@api.route("/api/signin")
class admin_registration(Resource):

    @api.expect(user_definition)
    def post(self):
        data = request.get_json()
        response = requests.post('http://oauth:5000/signin', json={'login': data.get('login'),
                                                                   'password': data.get('password')})
        if response.status_code == 200:
            return response.json(), 200
        else:
            return {}, response.status_code


@api.route("/api/signout")
class admin_registration(Resource):

    @api.expect(token_model)
    def post(self):
        data = request.get_json()
        response = requests.post('http://oauth:5000/signout', json={'token': data.get('token')})
        if response.status_code == 200:
            return response.json(), 200
        else:
            return {}, response.status_code
