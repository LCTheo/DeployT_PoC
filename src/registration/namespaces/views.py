from flask import request
from flask_restx import Namespace, Resource
import hashlib

from .models import user_definition_model, User, username_model, Attribute_Change_model

api = Namespace('views', description='route of the api', path="/")


@api.route("/registration/user")
class registrationUser(Resource):

    @api.expect(user_definition_model)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user = User(username=username, password=hashlib.sha512(password.encode("utf-8")).hexdigest(), testField=None)
        if user.save(force_insert=True):
            return {'state': "OK"}, 200
        else:
            return {'state': "fail"}, 200

    @api.expect(username_model)
    def delete(self):
        data = request.get_json()
        username = data.get('username')
        user = User.objects(username=username).first()
        if user:

            user.delete()
            return {'state': "OK"}, 200
        else:
            return {'state': "fail"}, 200


@api.route("/userInfo/<string:username>/<string:field>")
class registrationUser(Resource):

    @api.expect(Attribute_Change_model)
    def post(self, username, field):
        data = request.get_json()
        user = User.objects(username=username).first()
        if user:
            if field in user:
                if field == "password":
                    user.password = hashlib.sha512(data.get('new_value').encode("utf-8")).hexdigest()
                else:
                    user[field] = data.get('new_value')
                    user.save()
                return {}, 200
            else:
                return {}, 400
        return {}, 400
