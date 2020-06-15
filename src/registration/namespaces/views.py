from flask import request
from flask_restx import Namespace, Resource
import hashlib

from .models import user_definition, User, user_id, Admin
import dbFunction

api = Namespace('views', description='route of the api', path="/")

userTable = dbFunction.UserTableHandler(api, "user")
adminTable = dbFunction.UserTableHandler(api, "admin")


@api.route("/registration/user")
class registrationUser(Resource):

    @api.expect(user_definition)
    def post(self):
        data = request.get_json()
        login = data.get('login')
        password = data.get('password')
        user = User(login=login, password=hashlib.sha512(password.encode("utf-8")).hexdigest())
        if user.save(force_insert=True):
            return {'state': "OK"}, 200
        else:
            return {'state': "fail"}, 200

    @api.expect(user_id)
    def delete(self):
        data = request.get_json()
        user_id = data.get('user_id')
        user = User.objects(id=user_id)
        if user:
            user.delete()
            return {'state': "OK"}, 200
        else:
            return {'state': "fail"}, 200


@api.route("/registration/admin")
class registrationAdmin(Resource):

    @api.expect(user_definition)
    def post(self):
        data = request.get_json()
        login = data.get('login')
        password = data.get('password')
        admin = Admin(login=login, password=hashlib.sha512(password.encode("utf-8")).hexdigest())
        if admin.save(force_insert=True):
            return {'state': "OK"}, 200
        else:
            return {'state': "fail"}, 200

    @api.expect(user_definition)
    def delete(self):
        data = request.get_json()
        login = data.get('login')
        password = data.get('password')
        admin = Admin.objects(login=login, password=hashlib.sha512(password.encode("utf-8")).hexdigest())
        if admin:
            admin.delete()
            return {'state': "OK"}, 200
        else:
            return {'state': "fail"}, 200