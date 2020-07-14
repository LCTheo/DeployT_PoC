from flask_restx import fields, Namespace
import mongoengine as me


api = Namespace('models', description='all models used')

TYPE = ('small', 'medium', 'big')

REPO_TYPE = ['private', 'public']

STATUS = ('running', 'stopped')


# from registration .models
class User(me.Document):
    username = me.StringField(unique=True, required=True)
    password = me.StringField(required=True)
    testField = me.StringField(default="")


class Image(me.Document):
    imageId = me.StringField(primary_key=True, required=True)
    owner = me.ReferenceField(User, required=True)
    repository_url = me.URLField(required=True)
    repository_type = me.StringField(required=True, choices=REPO_TYPE)
    image_tag = me.StringField(required=True)
    config_file_path = me.StringField(required=True)


class Container(me.EmbeddedDocument):
    containerId = me.StringField(required=True, unique=True)
    imageId = me.StringField(required=True)
    environment = me.ListField(me.StringField())
    network = me.ListField(me.StringField())
    exposedPort = me.ListField(me.IntField())
    status = me.StringField(required=True, choices=STATUS, default='stopped')


class Network(me.EmbeddedDocument):
    networkId = me.StringField(required=True)


class Project(me.Document):
    name = me.StringField(required=True)
    owner = me.ReferenceField(User, required=True, unique_with=['name'])
    type = me.StringField(required=True, choices=TYPE)
    containers = me.MapField(me.EmbeddedDocumentField(Container))
    networks = me.MapField(me.EmbeddedDocumentField(Network))


project_setting = api.model('project setting', {
    'project_name': fields.String(required=True),
    'owner': fields.String(required=True),
    'project_type': fields.String(required=True, enum=TYPE)
})

dockerfile_setting = api.model('dockerfile setting', {
    'name': fields.String(required=True),
    'repository_URL': fields.String(required=True),
    'repo_visibility': fields.String(required=True, enum=['public', 'private']),
    'config_file_path': fields.String(required=True, default=".", example="."),

    'environment': fields.List(fields.String(required=True, pattern="[A-Z0-9-_]+=[a-zA-Z0-9-_]+", example="KEY=value")),
    'network': fields.List(fields.String(required=True, pattern="[a-zA-Z0-9-_]+", example="network")),
    'exposedPort': fields.List(fields.Integer(), required=True, default=[])

})

compose_setting = api.model('compose setting', {
    'repository_URL': fields.String(required=True),
    'repo_visibility': fields.String(required=True, enum=['public', 'private']),
    'config_file_path': fields.String(required=True, default=".", example="."),
})

getID = api.model('get project ID', {
    'project_name': fields.String(required=True),
    'owner': fields.String(required=True)
})

ProjectID = api.model('project ID', {
    'projectId': fields.String(required=True)
})

container = api.model('container name', {
    'container_name': fields.String(required=True)
})

manage_project = api.inherit('manage project', container, {
    'action': fields.String(required=True, enum=['start', 'stop']),
})
