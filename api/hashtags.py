from flask_accept import accept
from flask_restplus import Resource

from api import api

ns = api.namespace('hashtags', description='hashtags resource of tweets')

@ns.route("/")
class hashtags(Resource):
    @accept('application/json')
    def get(self):
        """search hashtags from tweets"""
        return []

