from flask_restx import Api

from .models import api as ns1
from .views import api as ns2

api = Api(version='0.4',
          title='DeployT API',
          validate=True
          )

api.add_namespace(ns1)
api.add_namespace(ns2)
