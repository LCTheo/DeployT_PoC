from flask import request
from flask_restx import Namespace, Resource
import requests

from core import DockerContainer, lisToDict
from .models import options

api = Namespace('views', description='route of the api', path="/")
client = DockerContainer()


@api.route("/deployment/<string:image>")
class deployment(Resource):

    @api.expect(options)
    def post(self, image):
        """docker run"""
        data = request.get_json()
        exist = client.imageExist(image)
        if exist == "0":
            labels = lisToDict(data.get('labels'))
            deprep = client.deploy(image, data.get('name'), data.get('hostname'), data.get('environment'), labels,
                                   data.get('network'))
            if deprep == "0":
                return {}, 200
            else:
                return {'code': deprep}, 400
        else:
            return {'code': exist}, 400


@api.route("/manage/<string:container>")
class manage(Resource):

    def get(self, container):
        """get container data"""
        code, container = client.getContainer(container)
        if code == "0":
            return container.labels, 200
        else:
            return {'code': code}, 400

    def delete(self, container):
        """docker rm"""
        rm = client.deleteContainer(container)
        if rm == "0":
            return {}, 200
        else:
            return {'code': rm}, 400


@api.route("/network/<string:networkId>")
class manage(Resource):

    def get(self, networkId):
        """get network data"""
        res = client.getNetwork(networkId)
        if res == "0":
            return {}, 200
        else:
            return {'code': res}, 400

    def post(self, networkId):
        res = client.createNetwork(networkId)
        if res == "0":
            return {}, 200
        else:
            return {'code': res}, 400

    def delete(self, networkId):
        """delete network"""
        res = client.deleteNetwork(networkId)
        if res == "0":
            return {}, 200
        else:
            return {'code': res}, 400
