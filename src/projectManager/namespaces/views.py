from flask import request
from flask_restx import Namespace, Resource

from core.projects import deleteContainer
from .models import project_setting, Project, User, dockerfile_setting, getID, container, ProjectID
from core import addContainer, getProjectId, deleteProject

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
class Container(Resource):

    @api.expect(dockerfile_setting)
    def post(self, projectId):
        data = request.get_json()
        rep = addContainer(projectId, data.get('name'), data.get('repository_URL'), data.get('repo_visibility'),
                           data.get('config_file_path'), data.get('environment'), data.get('network'),
                           data.get('exposedPort'))
        if rep == "0":
            return {'state': "done"}, 200
        else:
            return {'state': "fail", "code": rep}, 400


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
        data = request.get_json()
        res = deleteContainer(projectId, data.get('container_name'))
        if res == "0":
            return {}, 200
        else:
            return {'code': res}, 400