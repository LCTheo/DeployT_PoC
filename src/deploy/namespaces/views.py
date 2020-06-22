from flask import request
from flask_restx import Namespace, Resource
import requests

from core import DockerClient, lisToDict
from .models import options

api = Namespace('views', description='route of the api', path="/")
client = DockerClient()


@api.route("/deployment/<string:image>")
class deployment(Resource):

    @api.expect(options)
    def post(self, image):
        """docker run"""
        data = request.get_json()
        if client.imageExist(image):
            labels = lisToDict(data.get('labels'))
            if client.deploy(image, data.get('name'), data.get('hostname'), data.get('environment'), labels,
                             data.get('network')):
                return {}, 200
            else:
                return {}, 400


@api.route("/manage/<string:container>")
class manage(Resource):

    def get(self, container):
        """get container data"""
        container = client.getContainer(container)
        if container == -1:
            return {}, 400
        else:
            return container.labels, 200

    @api.expect(options)
    def put(self, container):
        """restart container"""
        return {}, 200

    def delete(self, container):
        """docker rm"""
        if client.deleteContainer(container) == 0:
            return {}, 200
        else:
            return {}, 400
