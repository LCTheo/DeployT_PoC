from flask import request
from flask_restx import Namespace, Resource
import requests

from core import DockerClient
from .models import options

api = Namespace('views', description='route of the api', path="/")
client = DockerClient()


@api.route("/deployment/<string:username>/<string:image>")
class deployment(Resource):

    @api.expect(options)
    def post(self, username, image):
        """docker run"""
        tag = image.split(":")
        rep = client.deploy("testapp:latest")
        api.logger.error(rep)
        return {}, 200

    @api.expect(options)
    def delete(self, user, image):
        """docker stop"""
        return {}, 200


@api.route("/reload/<string:username>/<string:container>")
class reload(Resource):

    @api.expect(options)
    def put(self, username, container):
        """rebuild du container"""
        return {}, 200











