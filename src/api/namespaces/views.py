from flask import request
from flask_restx import Namespace, Resource

import requests
from .models import user_definition, delete_model, token_model, setting_model, project_setting, container_setting, \
    containerId, manage_project
from core import getService

api = Namespace('views', description='route of the api', path="/")


@api.route("/api/status")
class status(Resource):

    def get(self):
        address = getService("register")
        if address[0] == "0":
            response = requests.get('http://' + address[1] + ':5000/status')
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
        if address[0] == "0":
            response = requests.post('http://' + address[1] + ':5000/registration/user',
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
        if address[0] == "0":
            validation = requests.get('http://' + address[1] + ':5000/validate',
                                      json={'token': data.get('token'),
                                            'username': data.get('username')})
            if validation.status_code == 200:
                address = getService("registration")
                if address[0] == "0":
                    response = requests.delete('http://' + address[1] + ':5000/registration/user',
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
        if address[0] == "0":
            response = requests.post('http://' + address[1] + ':5000/signin', json={'username': data.get('username'),
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
        if address[0] == "0":
            response = requests.post('http://' + address[1] + ':5000/signout',
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
        if address[0] == "0":
            validation = requests.get('http://' + address[1] + ':5000/validate',
                                      json={'token': data.get('token'),
                                            'username': data.get('username')})
            if validation.status_code == 200:
                address = getService("registration")
                if address[0] == "0":
                    response = requests.post(
                        'http://' + address[1] + ':5000/userInfo/' + data.get('username') + '/'
                        + data.get('field_name'), json={'new_value': data.get('new_value')})
                    if response.status_code == 200:
                        return {'state': "done"}
                    else:
                        return {'error': "unknown"}, 400
            else:
                return {}, 401
        else:
            return {}, 400


@api.route("/api/project/create")
class createProject(Resource):
    """create project"""

    @api.expect(project_setting)
    def post(self):
        data = request.get_json()
        address = getService("oauth")
        if address[0] == "0":
            validation = requests.get('http://' + address[1] + ':5000/validate',
                                      json={'token': data.get('token'),
                                            'username': data.get('username')})
            if validation.status_code == 200:
                address = getService("project")
                if address[0] == "0":
                    response = requests.post(
                        'http://' + address[1] + ':5000/project',
                        json={'project_name': data.get('project_name'), 'owner': data.get('username'),
                              'project_type': data.get('project_type')})
                    if response.status_code == 200:
                        return {'state': "done", 'projectId': response.json()['projectid']}
                    else:
                        return {'error': "06X"+str(response.status_code)}, 400
            else:
                return {}, 401
        else:
            return {}, 400


@api.route("/api/project/<string:projectId>")
class manageProject(Resource):
    """delete project"""

    @api.expect(token_model)
    def delete(self, projectId):
        return {}, 200

    """get project container"""

    @api.expect(token_model)
    def get(self, projectId):
        return {}, 200

    """start, stop or restart project"""

    @api.expect(manage_project)
    def post(self, projectId):
        return {}, 200


@api.route("/api/project/<string:projectId>/container")
class manageContainer(Resource):
    """add container"""

    @api.expect(container_setting)
    def post(self, projectId):
        return {}, 200

    """delete container"""

    @api.expect(containerId)
    def delete(self, projectId):
        return {}, 200

    """get container info"""

    @api.expect(containerId)
    def get(self, projectId):
        return {}, 200
