from flask_restx import fields, Namespace


api = Namespace('models', description='all models used')

options = api.model('options', {
    'name': fields.String(required=True),
    'hostname': fields.String(required=True),
    'environment ': fields.List(fields.String(pattern="[a-zA-Z0-9-_]+=[a-zA-Z0-9-_]+", example="key=value")),
    'labels': fields.List(fields.String(pattern="[a-zA-Z0-9-_]+:[a-zA-Z0-9-_]+", example="key:value")),
    'network': fields.List(fields.String(pattern="[a-zA-Z0-9-_]+", example="network")),

})
