import flask
from flask_restx import Api

from .models import api as ns1
from .views import api as ns2

api = Api(version='0.5',
          title='DeployT API',
          description="An api to deploy container on a host. "
                      "made by Le Coz Théo for a ENSIBS project",
          contact="https://github.com/LCTheo",
          validate=True
          )

api.add_namespace(ns1)
api.add_namespace(ns2)
