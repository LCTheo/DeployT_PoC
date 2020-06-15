from flask import Flask
from flask_cors import CORS
from namespaces import api

app = Flask(__name__)
CORS(app)
api.init_app(app)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
