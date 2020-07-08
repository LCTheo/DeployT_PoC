import os
import yaml
from flask import request
from flask_restx import Namespace, Resource

from .models import registrationArg

api = Namespace('views', description='route of the api', path="/")

serviceName = os.getenv('name')
with open('./services.yml') as f:
    services = yaml.load(f, Loader=yaml.FullLoader)
    for key in services:
        services[key]['address'] = []
    services['register']['address'].append(serviceName)


@api.route("/status")
class status(Resource):

    def get(self):
        serviceStatus = []
        for key in services:
            if len(services[key]['address']) == 0:
                serviceStatus.append([key, 'offline'])
            else:
                serviceStatus.append([key, 'online'])
        return {'status': serviceStatus}, 200


@api.route("/registration")
class registration(Resource):

    @api.response(200, 'Registration : Success')
    @api.response(400, 'Registration : error')
    @api.expect(registrationArg)
    def post(self):
        global services
        data = registrationArg.parse_args(request)
        if data.get('type') in services:
            service = services[data.get('type')]
            if service['card'] > len(service['address']):
                service['address'].append(data.get('address'))
                return {'registration': 'success'}, 200
            else:
                return {'registration': 'error'}, 400
        else:
            return {'registration': 'error'}, 404


@api.route("/address/<string:service>")
class getaddress(Resource):

    def get(self, service):
        if service in services:
            if len(services[service]['address']) > 0:
                address = services[service]['address'][0]
                return {'address': address}, 200
            else:
                return {}, 400
        else:
            return {}, 404
