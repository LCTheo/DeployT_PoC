from flask import request
from flask_restx import Namespace, Resource

from core import DockerImage
from .models import build, image_id, image_tag

api = Namespace('views', description='route of the api', path="/")
client = DockerImage()


@api.route("/image/build")
class deployment(Resource):

    @api.expect(build)
    def post(self):
        """docker build"""
        data = request.get_json()
        path = data.get('config_file_path')
        if not path:
            path = "."
        code, image = client.build(data.get('repository_URL'), data.get('image_tag'), path)
        if code == "0":
            return {'image': image.id}, 200
        else:
            return {'code': code}, 400

    @api.expect(image_id)
    def delete(self):
        """docker rmi"""
        data = request.get_json()
        client.delete(data.get('id'))
        return {}, 200


@api.route("/image/pull")
class pull(Resource):

    @api.expect(image_tag)
    def post(self):
        data = request.get_json()
        code, imageId = client.pull(data.get('image_tag'))
        if code == "0":
            return {'image': imageId}, 200
        else:
            return {'code': code}, 400
