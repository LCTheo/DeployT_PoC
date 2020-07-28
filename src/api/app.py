import os
from flask import Flask
from flask_cors import CORS
from namespaces import api, specs_url
from core import init


app = Flask(__name__)
CORS(app)
api.init_app(app)
api.specs_url = specs_url
serviceName = os.getenv('name')
if init(app.logger, serviceName) == 1:
    exit(1)


if __name__ == "__main__":
    app.run(host='0.0.0.0', ssl_context='adhoc')
