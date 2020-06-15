import time
from flask import Flask
import os
from flask_cors import CORS
import requests
from namespaces import api


app = Flask(__name__)
CORS(app)
api.init_app(app)
registerAddress = "register"
serviceName = os.getenv('name')
payload = {'type': 'api', 'address': os.getenv('name')}
r = requests.post('http://register:5000/registration', params=payload)
atempt = 1
while r.status_code != 200:
    if atempt == 3:
        app.logger.error('error while api registration')
        exit(1)
    time.sleep(5)
    r = requests.post('http://register:5000/registration', params=payload)
    atempt += 1
app.logger.info('api successfully registered')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
