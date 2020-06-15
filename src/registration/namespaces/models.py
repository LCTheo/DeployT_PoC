from flask_restx import Namespace, fields
import mongoengine as me

api = Namespace('models', description='all models used')

user_definition = api.model('User Informations', {
    'login': fields.String(required=True),
    'password': fields.String(required=True)
})

Attribute_Change = api.model('Attribute modification', {
    'login': fields.String(required=True),
    'newAttribute': fields.String(required=True)
})

user_id = api.model('user_id', {
    'user_id': fields.String(required=True)
})


class User(me.Document):
    login = me.StringField(unique=True)
    password = me.StringField()


class Admin(me.Document):
    login = me.StringField(unique=True)
    password = me.StringField()




