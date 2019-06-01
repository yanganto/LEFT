from flask_restplus import fields, reqparse


from api import api


account_info = api.model('AccountInfo', {
    'id': fields.Integer(description='The user id', readonly=True),
    'fullname': fields.String(description='The user name', readonly=True),
    'href': fields.String(description='The user href', readonly=True),
})

tweet_info = api.model('TweetInfo', {
    'account': fields.Nested(account_info, readonly=True),
    'date': fields.String(description='The date of tweet', readonly=True),
    'hashtags': fields.List(fields.String(required=False), default=[], readonly=True),
    'likes': fields.Integer(description='The number of likes of tweet', readonly=True),
    'replies': fields.Integer(description='The number of replies of tweet', readonly=True),
    'retweets': fields.Integer(description='The number of retweets of tweet', readonly=True),
    'text': fields.String(description='The text content of tweet', readonly=True),
})

query_parameter = reqparse.RequestParser()
query_parameter.add_argument('limit', type=int, help='The number of tweets', default=30)
