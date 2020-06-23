from flask import request
from flask_restx import Namespace, Resource
import requests

from core import DockerImage, lisToDict
from .models import build

api = Namespace('views', description='route of the api', path="/")
client = DockerImage()


@api.route("/image/build")
class deployment(Resource):

    @api.expect(build)
    def post(self):
        """docker build"""
        data = request.get_json()
        res = client.clone(data.get('repository_URL'), data.get('image_tag'), data.get('config_file_path'))
        return {"image": res[0].tags}, 200
