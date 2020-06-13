import time
from flask import Flask, request, send_file, render_template
from flask_restx import Api, Resource, reqparse, fields
import os
from flask_cors import CORS
from flask_mongoengine import MongoEngine
import mongoengine as me
import requests
import dbFunction

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    "db": "UserDb",
    "host": "mongodb://mongo:27017/"
}
db = MongoEngine(app)
CORS(app)
api = Api(app=app, version='0.1', validate=True) #, doc=False
user_definition = api.model('User Informations', {
    'login': fields.String(required=True),
    'password': fields.String(required=True)
})
Attribute_Change = api.model('Attribute modification', {
    'login': fields.String(required=True),
    'newAttribute': fields.String(required=True)
})
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
userTable = dbFunction.UserTableHandler(app, "user")
adminTable = dbFunction.UserTableHandler(app, "admin")


class User(me.EmbeddedDocument):
    id = me.IntField(primary_key=True)
    username = me.StringField(unique=True)
    password = me.StringField()


@api.route("/registration/user")
class registrationUser(Resource):

    @api.expect(user_definition)
    def post(self):
        data = request.get_json()
        login = data.get('login')
        password = data.get('password')
        res = userTable.add(login, password)
        return {'res': res}, 200

    @api.expect(user_definition)
    def delete(self):
        data = request.get_json()
        login = data.get('login')
        password = data.get('password')
        res = userTable.delete(login, password)
        return {'res': res}, 200


@api.route("/registration/admin")
class registrationAdmin(Resource):

    @api.expect(user_definition)
    def post(self):
        data = request.get_json()
        login = data.get('login')
        password = data.get('password')
        res = adminTable.add(login, password)
        return {'res': res}, 200

    @api.expect(user_definition)
    def delete(self):
        data = request.get_json()
        login = data.get('login')
        password = data.get('password')
        res = adminTable.delete(login, password)
        return {'res': res}, 200


@api.route("/registration/<string:consumer>/<string:attribute>")
class registration(Resource):

    @api.expect(Attribute_Change)
    def put(self, consumer, attribute):
        data = request.get_json()
        login = data.get('login')
        newAttribute = data.get('newAttribute')
        if consumer == "user":
            res = userTable.modify(login, attribute, newAttribute)
        elif consumer == "admin":
            res = adminTable.modify(login, attribute, newAttribute)
        else:
            return {}, 404
        return {'res': res}, 200


if __name__ == "__main__":
    app.run(host='0.0.0.0')
