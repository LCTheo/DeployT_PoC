from flask_restx import Api
from .models import api as ns1
from .views import api as ns2

api = Api(version='0.5',
          validate=True,
          doc=False
          )

api.add_namespace(ns1)
api.add_namespace(ns2)
