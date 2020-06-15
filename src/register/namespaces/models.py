from flask_restx import Namespace, reqparse

api = Namespace('models', description='all models used')

registrationArg = reqparse.RequestParser()
registrationArg.add_argument('type', type=str, required=True)
registrationArg.add_argument('address', type=str, required=True)






