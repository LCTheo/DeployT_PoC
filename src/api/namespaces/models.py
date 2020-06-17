from flask_restx import fields, Namespace


api = Namespace('models', description='all models used')

user_definition = api.model('User Informations', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

token_model = api.model('token', {
    'token': fields.String(required=True)
})

delete_model = api.inherit('delete', token_model, {
    'username': fields.String(required=True)
})

setting_model = api.inherit('field modification', token_model, {
    'username': fields.String(required=True),
    'field_name': fields.String(required=True),
    'new_value': fields.String(required=True)
})
