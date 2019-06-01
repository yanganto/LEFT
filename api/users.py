from flask_accept import accept
from flask_restplus import Resource

from api import api
from api.model import tweet_info, query_parameter
from utils.twitter_requests import TwitterRequests, TwitterConnectionError

ns = api.namespace('users', description='users resource of tweets')

@ns.route("/<string:user_name>")
class Users(Resource):
    @accept('application/json')
    @ns.expect(query_parameter)
    @api.response(200, "Success")
    @api.response(503, 'Twitter Service Down')
    @ns.marshal_list_with(tweet_info)
    def get(self, user_name):
        """search users from tweets"""
        try:
            args = query_parameter.parse_args()
            return TwitterRequests().query('@' + user_name,
                                           count=args.get('limit', 30))
        except TwitterConnectionError:
            return "Twitter Service Down", 503
