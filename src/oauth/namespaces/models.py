from flask_restx import Namespace, fields
import mongoengine as me

api = Namespace('models', description='all models used')

user_auth = api.model('User Informations', {
    'login': fields.String(required=True),
    'password': fields.String(required=True)
})

validation = api.model('validation', {
    'user_id': fields.String(required=True),
    'token': fields.String(required=True)
})

token_model = api.model('token', {
    'token': fields.String(required=True)
})


class User(me.Document):
    id = me.IntField(primary_key=True)
    login = me.StringField(unique=True)
    password = me.StringField()


class Token(me.Document):
    id = me.IntField(primary_key=True)
    user_id = me.IntField(required=True)
    access_token = me.StringField(unique=True)
    expires = me.DateTimeField





