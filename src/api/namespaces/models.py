from flask_restx import fields, Namespace


api = Namespace('models', description='all models used')

user_definition = api.model('User Informations', {
    'login': fields.String(required=True),
    'password': fields.String(required=True)
})

token_model = api.model('token', {
    'token': fields.String(required=True)
})

delete_model = api.inherit('delete', token_model, {
    'user_id': fields.String(required=True)
})
