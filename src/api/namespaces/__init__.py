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


@property
def specs_url(self):
    """Fixes issue where swagger-ui makes a call to swagger.json over HTTP.
       This can ONLY be used on servers that actually use HTTPS.  On servers that use HTTP,
       this code should not be used at all.
    """
    return flask.url_for(self.endpoint('specs'), _external=True, _scheme='https')