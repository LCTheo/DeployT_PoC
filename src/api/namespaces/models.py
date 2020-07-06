from flask_restx import fields, Namespace

api = Namespace('models', description='all models used')

user_definition = api.model('User Informations', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

token_model = api.model('token', {
    'token': fields.String(required=True),
    'username': fields.String(required=True)
})

delete_model = api.inherit('delete', token_model, {
    'username': fields.String(required=True)
})

setting_model = api.inherit('field modification', token_model, {
    'username': fields.String(required=True),
    'field_name': fields.String(required=True),
    'new_value': fields.String(required=True)
})

project_setting = api.inherit('project setting', token_model, {
    'project_name': fields.String(required=True),
    'project_type': fields.String(required=True, enum=['small', 'medium', 'big'])

})

container_setting = api.inherit('container setting', token_model, {
    'config_type': fields.String(required=True, enum=['Dockerfile', 'Compose']),
    'repository_URL': fields.String(required=True),
    'repo_visibility': fields.String(required=True, enum=['public', 'private']),
    'config_file_path': fields.String(required=True, default="."),

    # if dockerfile type
    'name': fields.String,
    'environment ': fields.List(fields.String(pattern="[a-zA-Z0-9-_]+=[a-zA-Z0-9-_]+", example="key=value")),
    'network': fields.List(fields.String(pattern="[a-zA-Z0-9-_]+", example="network")),
    'exposedPort': fields.List(fields.Integer)

    # if compose type
})

containerId = api.inherit('container Id', token_model, {
    'containerId': fields.String(required=True)
})

manage_project = api.inherit('manage project', token_model, {
    'action': fields.String(required=True, enum=['start', 'stop', 'restart']),
    'container_list': fields.List(fields.String)
})
