import logging

from flask_accept import accept
from flask_restplus import Resource

from api import api
from api.model import tweet_info, query_parameter, status_formator
from utils.twitter_requests import TwitterRequests, TwitterConnectionError

logger = logging.getLogger(__name__)
ns = api.namespace('users', description='users resource of tweets')

@ns.route("/<string:user_name>")
class Users(Resource):
    @accept('application/json', 'application/anymind.left.v1+json')
    @ns.expect(query_parameter)
    @api.response(200, "Success")
    @api.response(503, 'Twitter Service Down')
    @ns.marshal_list_with(tweet_info)
    def get(self, user_name):
        """search users from tweets"""
        try:
            args = query_parameter.parse_args()
            return [status_formator(s)
                    for s in TwitterRequests().user_timeline(user_name,
                                                             count=args.get('limit', 30))]
        except TwitterConnectionError:
            logger.exception("Twitter Service Down")
            return "Twitter Service Down", 503
