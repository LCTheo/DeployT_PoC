import os
from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from namespaces import api
from core import init

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    "db": "UserDb",
    "host": "mongodb://mongo:27017/UserDb"
}
db = MongoEngine(app)
CORS(app)
api.init_app(app)

serviceName = os.getenv('name')
if init(app.logger, serviceName) == 1:
    exit(1)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
