from flask import request
from flask_restx import Namespace, Resource

import requests
from .models import user_definition, delete_model, token_model, setting_model, project_setting, container_setting, \
    manage_project, container_list
from core import getService

api = Namespace('views', description='route of the api', path="/")


@api.route("/api/status")
class status(Resource):

    def get(self):
        """see the status of all internal service"""
        code, address = getService("register")
        if code == "0":
            response = requests.get('http://' + address + ':5000/status')
            r = response.json()
            return r, 200
        else:
            return {}, 400


@api.route("/api/user/registration")
class user_registration(Resource):

    @api.expect(user_definition)
    def post(self):
        """create a new user"""
        data = request.get_json()
        code, address = getService("registration")
        if code == "0":
            response = requests.post('http://' + address + ':5000/registration/user',
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
        """delete form the database the user"""
        data = request.get_json()
        code, address = getService("oauth")
        if code == "0":
            validation = requests.get('http://' + address + ':5000/validate',
                                      json={'token': data.get('token'),
                                            'username': data.get('username')})
            if validation.status_code == 200:
                code, address = getService("registration")
                if code == "0":
                    response = requests.delete('http://' + address + ':5000/registration/user',
                                               json={'token': data.get('token')})
                    if response.status_code == 200:
                        return response.json(), 200
                    else:
                        return {}, response.status_code
            elif validation.status_code == 400:
                return {'token': 'expired'}, 400
            else:
                return {}, 404
        else:
            return {}, 401


@api.route("/api/signin")
class signin(Resource):

    @api.expect(user_definition)
    def post(self):
        """sign in to get a token"""
        data = request.get_json()
        code, address = getService("oauth")
        if code == "0":
            response = requests.post('http://' + address + ':5000/signin',
                                     json={'username': data.get('username'),
                                           'password': data.get('password')})
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
        """sign out to revoke the token"""
        data = request.get_json()
        code, address = getService("oauth")
        if code == "0":
            response = requests.post('http://' + address + ':5000/signout',
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
        """modify a user information like password.

        example:
            'field_name': 'password'
            'new_value': 'myNewPassword'
            """
        data = request.get_json()
        code, address = getService("oauth")
        if code == "0":
            validation = requests.get('http://' + address + ':5000/validate',
                                      json={'token': data.get('token'),
                                            'username': data.get('username')})
            if validation.status_code == 200:
                code, address = getService("registration")
                if code == "0":
                    response = requests.post(
                        'http://' + address + ':5000/userInfo/' + data.get('username') + '/'
                        + data.get('field_name'), json={'new_value': data.get('new_value')})
                    if response.status_code == 200:
                        return {'state': "done"}, 200
                    else:
                        return {'error': "unknown"}, 400
            elif validation.status_code == 400:
                return {'token': 'expired'}, 400
            else:
                return {}, 404
        else:
            return {}, 401


@api.route("/api/project/create")
class createProject(Resource):

    @api.expect(project_setting)
    def post(self):
        """create project
        project type have no incidence yet"""
        data = request.get_json()
        code, address = getService("oauth")
        if code == "0":
            validation = requests.get('http://' + address + ':5000/validate',
                                      json={'token': data.get('token'),
                                            'username': data.get('username')})
            if validation.status_code == 200:
                code, address = getService("project")
                if code == "0":
                    response = requests.post(
                        'http://' + address + ':5000/project',
                        json={'project_name': data.get('project_name'), 'owner': data.get('username'),
                              'project_type': data.get('project_type')})
                    if response.status_code == 200:
                        return {'state': "done", 'projectId': response.json()['projectid']}, 200
                    else:
                        return {'error': "04X" + str(response.status_code)}, 400
            elif validation.status_code == 400:
                return {'token': 'expired'}, 400
            else:
                return {}, 404
        else:
            return {}, 401


@api.route("/api/project/list")
class listProject(Resource):

    @api.expect(token_model)
    def post(self):
        """list all current project"""
        data = request.get_json()
        code, address = getService("oauth")
        if code == "0":
            validation = requests.get('http://' + address + ':5000/validate',
                                      json={'token': data.get('token'),
                                            'username': data.get('username')})
            if validation.status_code == 200:
                code, address = getService("project")
                if code == "0":
                    response = requests.get('http://' + address + ':5000/project',
                                            json={'username': data.get('username')})
                    if response.status_code == 200:
                        return {'state': "done", 'project_List': response.json()['project_list']}, 200
                    else:
                        return {'error': "04X" + str(response.status_code)}, 400
            elif validation.status_code == 400:
                return {'token': 'expired'}, 400
            else:
                return {}, 404
        else:
            return {}, 401


@api.route("/api/project/<string:projectName>")
class manageProject(Resource):

    @api.expect(token_model)
    def delete(self, projectName):
        """delete the given project"""
        data = request.get_json()
        code, address = getService("oauth")
        if code == "0":
            validation = requests.get('http://' + address + ':5000/validate',
                                      json={'token': data.get('token'),
                                            'username': data.get('username')})
            if validation.status_code == 200:
                code, address = getService("project")
                if code == "0":
                    responseID = requests.get('http://' + address + ':5000/getID',
                                              json={'project_name': projectName,
                                                    'owner': data.get('username')})
                    if responseID.status_code == 200:
                        response = requests.delete('http://' + address + ':5000/project',
                                                   json={'projectId': responseID.json()['project_id']})
                        if response.status_code == 200:
                            return {'state': "done"}, 200
                        elif response.status_code == 400:
                            return {'error': "04X" + response.json()['code']}, 400
                        else:
                            return {'error': "04X500"}, 400
                else:
                    return {}, 401
            elif validation.status_code == 400:
                return {'token': 'expired'}, 400
            else:
                return {}, 404
        else:
            return {}, 401

    @api.expect(manage_project)
    def post(self, projectName):
        """change the status of the container in the given project
        if container_list if empty then all container are included

        example:
            'action': 'start'
            'container_list': []
        it will start all containers of the given project
        """
        data = request.get_json()
        code, address = getService("oauth")
        if code == "0":
            validation = requests.get('http://' + address + ':5000/validate',
                                      json={'token': data.get('token'),
                                            'username': data.get('username')})
            if validation.status_code == 200:
                code, address = getService("project")
                if code == "0":
                    responseID = requests.get('http://' + address + ':5000/getID',
                                              json={'project_name': projectName,
                                                    'owner': data.get('username')})
                    if responseID.status_code == 200:
                        containers = data.get('container_list')
                        if containers is None:
                            containers = []
                        response = requests.post('http://' + address + ':5000/' + responseID.json()['project_id'],
                                                 json={'action': data.get('action'),
                                                       'container_list': containers})
                        if response.status_code == 200:
                            return {'state': "done"}, 200
                        elif response.status_code == 400:
                            return {'error': "04X" + response.json()['code']}, 400
                        else:
                            return {'error': "04X500"}, 400
                else:
                    return {}, 401
            elif validation.status_code == 400:
                return {'token': 'expired'}, 400
            else:
                return {}, 404
        else:
            return {}, 401


@api.route("/api/project/<string:projectName>/container")
class manageContainer(Resource):

    @api.expect(container_setting)
    def post(self, projectName):
        """add containers to the given project.
        there is two usage available
        from a compose file:
            if you want to add container with a docker-compose file then you need to only give the four first argument
            config_file_path is the path from the project root were is the docker-compose file
            example:
                'config_type': 'Compose'
                'repository_URL': 'https://github.com/LCTheo/securDoc.git'
                'repo_visibility': 'public'
                'config_file_path': '.'

                Warning!! : this example is not completely functional

        from Dockerfile:
        if you want to describe yourself the configuration you need at least the name in addition of
        the four first argument.
        config_file_path is the path from the project root were is the Dockerfile
        example:
            'config_type': 'Dockerfile'
            'repository_URL': 'https://github.com/LCTheo/testAPP.git'
            'repo_visibility':
            'public' 'config_file_path': '.'
            'name': 'myContainer'
            'environment': ['MY_VARIABLE=My_value']
            'network': ['myContainerNetwork']
            'exposedPort': [5000, 80]
        """
        data = request.get_json()
        code, address = getService("oauth")
        if code == "0":
            validation = requests.get('http://' + address + ':5000/validate',
                                      json={'token': data.get('token'),
                                            'username': data.get('username')})
            if validation.status_code == 200:
                code, address = getService("project")
                if code == "0":
                    responseID = requests.get('http://' + address + ':5000/getID',
                                              json={'project_name': projectName,
                                                    'owner': data.get('username')})
                    if responseID.status_code == 200:
                        project_id = responseID.json()['project_id']
                        if data.get('config_type') == 'Dockerfile':
                            if data.get('name'):
                                environment = data.get('environment')
                                exposedPort = data.get('exposedPort')
                                network = data.get('network')
                                if environment is None:
                                    environment = []
                                if exposedPort is None:
                                    exposedPort = []
                                if network is None:
                                    network = []
                                response = requests.post(
                                    'http://' + address + ':5000/container/' + project_id + '/dockerfile',
                                    json={'name': data.get('name'),
                                          'repository_URL': data.get('repository_URL'),
                                          'repo_visibility': data.get('repo_visibility'),
                                          'config_file_path': data.get('config_file_path'),
                                          'environment': environment,
                                          'network': network,
                                          'exposedPort': exposedPort})
                            else:
                                return {'error': "01X001", 'parameter': 'name'}, 400
                        elif data.get('config_type') == 'Compose':
                            response = requests.post(
                                'http://' + address + ':5000/container/' + project_id + '/compose',
                                json={'name': data.get('name'),
                                      'repository_URL': data.get('repository_URL'),
                                      'repo_visibility': data.get('repo_visibility'),
                                      'config_file_path': data.get('config_file_path')})
                        else:
                            return {'error': "01X001", 'parameter': 'config_type'}, 400

                        if response.status_code == 200:
                            return {'state': "done"}, 200
                        elif response.status_code == 400:
                            return {'error': "04X" + response.json()['code']}, 400
                        else:
                            return {'error': "04X500"}, 400
                    else:
                        return {}, 400
                else:
                    return {}, 401
            elif validation.status_code == 400:
                return {'token': 'expired'}, 400
            else:
                return {}, 404
        else:
            return {}, 401

    @api.expect(container_list)
    def delete(self, projectName):
        """delete the listed container from the project
        if container_list if empty then all container are included
        """
        data = request.get_json()
        code, address = getService("oauth")
        if code == "0":
            validation = requests.get('http://' + address + ':5000/validate',
                                      json={'token': data.get('token'),
                                            'username': data.get('username')})
            if validation.status_code == 200:
                code, address = getService("project")
                if code == "0":
                    responseID = requests.get('http://' + address + ':5000/getID',
                                              json={'project_name': projectName,
                                                    'owner': data.get('username')})
                    if responseID.status_code == 200:
                        containers = data.get('container_list')
                        if containers is None:
                            containers = []
                        response = requests.delete('http://' + address + ':5000/' + responseID.json()['project_id'],
                                                   json={'container_list': containers})
                        if response.status_code == 200:
                            return {'state': "done"}, 200
                        elif response.status_code == 400:
                            return {'error': "04X" + response.json()['code']}, 400
                        else:
                            return {'error': "04X500"}, 400
                else:
                    return {}, 401
            elif validation.status_code == 400:
                return {'token': 'expired'}, 400
            else:
                return {}, 404
        else:
            return {}, 401


@api.route("/api/project/<string:projectName>/info")
class containerInfo(Resource):

    @api.expect(container_list)
    def post(self, projectName):
        """get containers information
        if container_list if empty then all container are included"""
        data = request.get_json()
        code, address = getService("oauth")
        if code == "0":
            validation = requests.get('http://' + address + ':5000/validate',
                                      json={'token': data.get('token'),
                                            'username': data.get('username')})
            if validation.status_code == 200:
                code, address = getService("project")
                if code == "0":
                    responseID = requests.get('http://' + address + ':5000/getID',
                                              json={'project_name': projectName,
                                                    'owner': data.get('username')})
                    if responseID.status_code == 200:
                        containers = data.get('container_list')
                        if containers is None:
                            containers = []
                        response = requests.get('http://' + address + ':5000/' + responseID.json()['project_id'],
                                                json={'container_list': containers})
                        if response.status_code == 200:
                            return response.json(), 200
                        elif response.status_code == 400:
                            return {'error': "04X" + response.json()['code']}, 400
                        else:
                            return {'error': "04X500"}, 400
                else:
                    return {}, 401
            elif validation.status_code == 400:
                return {'token': 'expired'}, 400
            else:
                return {}, 404
        else:
            return {}, 401
