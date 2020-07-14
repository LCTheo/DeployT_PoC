from flask_restx import Api

from .models import api as ns1
from .views import api as ns2

api = Api(version='0.4',
          title='image building service',
          validate=True
          )

api.add_namespace(ns1)
api.add_namespace(ns2)
