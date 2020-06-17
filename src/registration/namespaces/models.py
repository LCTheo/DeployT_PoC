from flask_restx import Namespace, fields
import mongoengine as me

api = Namespace('models', description='all models used')

user_definition_model = api.model('User Informations', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

Attribute_Change_model = api.model('Attribute modification', {
    'new_value': fields.String(required=True)
})

username_model = api.model('username', {
    'username': fields.String(required=True)
})


class User(me.Document):
    username = me.StringField(unique=True, required=True)
    password = me.StringField(required=True)
    testField = me.StringField(default="")






