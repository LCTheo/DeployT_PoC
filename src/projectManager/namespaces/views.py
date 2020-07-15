from flask import request
from flask_restx import Namespace, Resource

from .models import project_setting, Project, User, dockerfile_setting, getID, container, ProjectID, manage_project, \
    compose_setting
from core import *

api = Namespace('views', description='route of the api', path="/")


@api.route("/project")
class Create(Resource):

    @api.expect(project_setting)
    def post(self):
        data = request.get_json()
        owner = User.objects(username=data.get('owner')).first()
        project = Project(name=data.get('project_name'), owner=owner, type=data.get('project_type'))
        project.save()
        return {'projectid': str(project.id)}, 200

    @api.expect(ProjectID)
    def delete(self):
        data = request.get_json()
        rep = deleteProject(data.get('projectId'))
        if rep == "0":
            return {'state': "done"}, 200
        else:
            return {'state': "fail", "code": rep}, 400


@api.route("/container/<string:projectId>/dockerfile")
class Dockerfile(Resource):

    @api.expect(dockerfile_setting)
    def post(self, projectId):
        data = request.get_json()
        code, image = addImage(projectId, data.get('name'), data.get('repository_URL'), data.get('repo_visibility'),
                               data.get('config_file_path'))
        if code == "0":
            rep = addContainer(projectId, data.get('name'), image, data.get('environment'), data.get('network'),
                               data.get('exposedPort'))
            if rep == "0":
                return {'state': "done"}, 200
            else:
                return {'state': "fail", "code": rep}, 400
        else:
            return {'state': "fail", "code": code}, 400


@api.route("/container/<string:projectId>/compose")
class Compose(Resource):

    @api.expect(compose_setting)
    def post(self, projectId):
        data = request.get_json()
        code, config = extractConfig(data.get('repository_URL'), data.get('repo_visibility'),
                                     data.get('config_file_path'))
        if code == "0":
            rep = redactContainer(config, projectId, "compose", data.get('repository_URL'))
            if rep == "0":
                return {'state': "done"}, 200
            else:
                return {'state': "fail", "code": rep}, 400
        else:
            return {'state': "fail", "code": code}, 400


@api.route("/getID")
class ProjectID(Resource):

    @api.expect(getID)
    def get(self):
        data = request.get_json()
        projectId = getProjectId(data.get('project_name'), data.get('owner'))
        if projectId:
            return {'project_id': projectId}, 200
        else:
            return {'code': "04001"}, 400


@api.route("/<string:projectId>")
class ManageContainer(Resource):

    @api.expect(container)
    def get(self):
        """get container Spec"""
        return {}, 200

    @api.expect(container)
    def delete(self, projectId):
        """delete containers"""
        data = request.get_json()
        res = deleteContainer(projectId, data.get('container_list'), api.logger)
        if res == "0":
            return {}, 200
        else:
            return {'code': res}, 400

    @api.expect(manage_project)
    def post(self, projectId):
        """start, stop containers"""
        data = request.get_json()
        res = containerStatus(projectId, data.get('container_list'), data.get('action'))
        if res == "0":
            return {}, 200
        else:
            return {'code': res}, 400
