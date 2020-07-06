from flask_restx import fields, Namespace


api = Namespace('models', description='all models used')


build = api.model('build parameter', {
    'repository_URL': fields.String(required=True),
    'repo_visibility': fields.String(required=True, enum=['public', 'private']),
    'image_tag': fields.String(required=True),
    'config_file_path': fields.String(default=".")

})

image_id = api.model('image id', {
    'id': fields.String(required=True)
})
