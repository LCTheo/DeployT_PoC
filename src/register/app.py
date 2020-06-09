import logging
import os

from flask import Flask, request
from flask_restx import Api, Resource, reqparse
from flask_cors import CORS
import yaml


app = Flask(__name__)
CORS(app)
api = Api(app=app, version='0.1', validate=True)  #, doc=False
registrationArg = reqparse.RequestParser()
registrationArg.add_argument('type', type=str, required=True)
registrationArg.add_argument('address', type=str, required=True)

serviceName = os.getenv('name')
with open('./services.yml') as f:
    services = yaml.load(f, Loader=yaml.FullLoader)
    for key in services:
        services[key]['address'] = []
    services['register']['address'].append(serviceName)


@api.route("/status")
class status(Resource):

    def get(self):
        status = []
        for key in services:
            if len(services[key]['address']) == 0:
                status.append([key, 'offline'])
            else:
                status.append([key, 'online'])
        return {'status': status}, 200


@api.expect(registrationArg)
@api.route("/registration")
class registration(Resource):

    @api.response(200, 'Registration : Success')
    @api.response(400, 'Registration : error')
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
                return {}, 204
        else:
            return {}, 404


if __name__ == "__main__":
    app.run(host='0.0.0.0')
