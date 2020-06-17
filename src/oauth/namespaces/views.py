import hashlib
from flask import request
from flask_restx import Namespace, Resource
from werkzeug.security import gen_salt
from datetime import datetime, timedelta

from .models import user_auth, User, token_model, validation, Token

api = Namespace('views', description='route of the api', path="/")


@api.route("/signin")
class access_token(Resource):

    @api.expect(user_auth)
    def post(self):
        data = request.get_json()
        user = User.objects(username=data.get('username')).first()
        if user:
            if user.password == hashlib.sha512(data.get('password').encode("utf-8")).hexdigest():
                if not Token.objects(username=user.username).first():
                    token = Token(username=user.username, access_token=gen_salt(50), expires=datetime.now() + timedelta(hours=1))
                    token.save(force_insert=True)
                    return {'token': token.access_token}, 200
                else:
                    return {'signin': True}, 200
            else:
                return {}, 401
        else:
            return {}, 402


@api.route("/signout")
class access_token(Resource):

    @api.expect(token_model)
    def post(self):
        data = request.get_json()
        token = Token.objects(access_token=data.get('token')).first()
        if token:
            token.delete()
            return {}, 200
        else:
            return {}, 401


@api.route("/validate")
class access_token(Resource):

    @api.expect(validation)
    def get(self):
        data = request.get_json()
        token = Token.objects(access_token=data.get('token')).first()
        if token and token.username == data.get('username'):
            if token.expires > datetime.now():
                return {'expires': False}, 200
            else:
                return {'expires': True}, 200
        else:
            return {}, 401
