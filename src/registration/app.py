import time
from flask import Flask
from flask_restx import Api
import os
from flask_cors import CORS
from flask_mongoengine import MongoEngine
import requests


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    "db": "UserDb",
    "host": "mongodb://mongo:27017/"
}
db = MongoEngine(app)
CORS(app)
api = Api(app=app, version='0.1', validate=True, doc=False)

registerAddress = "register"
serviceName = os.getenv('name')
payload = {'type': 'registration', 'address': os.getenv('name')}
r = requests.post('http://register:5000/registration', params=payload)
atempt = 1
while r.status_code != 200:
    if atempt == 3:
        app.logger.error('error while api registration')
        exit(1)
    time.sleep(1)
    r = requests.post('http://register:5000/registration', params=payload)
    atempt += 1
app.logger.info('registration successfully registered')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
