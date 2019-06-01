from flask_accept import accept
from flask_restplus import Resource

from api import api
from api.model import tweet_info, query_parameter
from utils.twitter_requests import TwitterRequests, TwitterConnectionError


ns = api.namespace('hashtags', description='hashtags resource of tweets')

@ns.route("/<string:tag>")
class hashtags(Resource):
    @accept('application/json')
    @ns.expect(query_parameter)
    @api.response(200, "Success")
    @api.response(503, 'Twitter Service Down')
    @ns.marshal_list_with(tweet_info)
    def get(self, tag):
        """search hashtags from tweets"""
        try:
            args = query_parameter.parse_args()
            return TwitterRequests().query('#' + tag,
                                           count=args.get('limit', 30))
        except TwitterConnectionError:
            return "Twitter Service Down", 503
