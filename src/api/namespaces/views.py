from flask import request
from flask_restx import Namespace, Resource

import requests
from .models import user_definition, delete_model, token_model, setting_model
from core import getService

api = Namespace('views', description='route of the api', path="/")


@api.route("/api/status")
class status(Resource):

    def get(self):
        address = getService("register")
        if 'address' in address:
            response = requests.get('http://' + address['address'] + ':5000/status')
            r = response.json()
            return r, 200
        else:
            return {}, 400


@api.route("/api/user/registration")
class user_registration(Resource):

    @api.expect(user_definition)
    def post(self):
        data = request.get_json()
        address = getService("registration")
        if 'address' in address:
            response = requests.post('http://' + address['address'] + ':5000/registration/user',
                                     json={'username': data.get('username'),
                                           'password': data.get(
                                               'password')})
            if response.status_code == 200:
                return response.json(), 200
            else:
                return {}, response.status_code
        else:
            return {}, 400

    @api.expect(delete_model)
    def delete(self):
        data = request.get_json()
        address = getService("oauth")
        if 'address' in address:
            validation = requests.get('http://' + address['address'] + ':5000/validate',
                                      json={'token': data.get('token'),
                                            'username': data.get('username')})
            if validation.status_code == 200:
                address = getService("registration")
                response = requests.delete('http://' + address['address'] + ':5000/registration/user',
                                           json={'token': data.get('token')})
                if response.status_code == 200:
                    return response.json(), 200
                else:
                    return {}, response.status_code
            else:
                return
        else:
            return {}, 400


@api.route("/api/signin")
class signin(Resource):

    @api.expect(user_definition)
    def post(self):
        data = request.get_json()
        address = getService("oauth")
        if 'address' in address:
            response = requests.post('http://' + address['address'] + ':5000/signin', json={'username': data.get('username'),
                                                                                            'password': data.get(
                                                                                                'password')})
            if response.status_code == 200:
                return response.json(), 200
            else:
                return {}, response.status_code
        else:
            return {}, 400


@api.route("/api/signout")
class signout(Resource):

    @api.expect(token_model)
    def post(self):
        data = request.get_json()
        address = getService("oauth")
        if 'address' in address:
            response = requests.post('http://' + address['address'] + ':5000/signout',
                                     json={'token': data.get('token')})
            if response.status_code == 200:
                return response.json(), 200
            else:
                return {}, response.status_code
        else:
            return {}, 400


@api.route("/api/setting")
class setting(Resource):

    @api.expect(setting_model)
    def put(self):
        data = request.get_json()
        address = getService("oauth")
        if 'address' in address:
            validation = requests.get('http://' + address['address'] + ':5000/validate',
                                      json={'token': data.get('token'),
                                            'username': data.get('username')})
            if validation.status_code == 200:
                address = getService("registration")
                if 'address' in address:
                    response = requests.post(
                        'http://' + address['address'] + ':5000/userInfo/' + data.get('username') + '/'
                        + data.get('field_name'), json={'new_value': data.get('new_value')})
                    if response.status_code == 200:
                        return {'state': "done"}
                    else:
                        return {'error': "unknown"}, 400
            else:
                return {}, 401
        else:
            return {}, 400
