from flask_restx import Namespace, fields
import mongoengine as me

api = Namespace('models', description='all models used')

user_auth = api.model('User Informations', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

validation = api.model('validation', {
    'username': fields.String(required=True),
    'token': fields.String(required=True)
})

token_model = api.model('token', {
    'token': fields.String(required=True)
})


class User(me.Document):
    username = me.StringField(unique=True, required=True)
    password = me.StringField(required=True)
    testField = me.StringField(default="")


class Token(me.Document):
    username = me.StringField(unique=True, required=True)
    access_token = me.StringField(unique=True, required=True)
    expires = me.DateTimeField(required=True)





