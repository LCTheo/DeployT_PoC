from flask_restx import fields, Namespace


api = Namespace('models', description='all models used')

options = api.model('options', {
    'token': fields.String(required=True)
})
