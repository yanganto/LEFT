from flask_accept import accept
from flask_restplus import Resource

from api import api

ns = api.namespace('users', description='users resource of tweets')

@ns.route("/")
class Users(Resource):
    @accept('application/json')
    def get(self):
        """search users from tweets"""
        return []

