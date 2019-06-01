import os
import sys

from flask import Flask, Blueprint, Response, request
from flask_restplus import Resource
import markdown2

from api import api
from api.hashtags import ns as hashtags_namespace
from api.users import ns as users_namespace
from utils.twitter_requests import TwitterRequests, TwitterKeyAbsentError

application = Flask(__name__)

# Be friendly for user to avoid tailling "/" issue
application.url_map.strict_slashes = False


@application.route("/")
def readme():
    """Provide readme on landing page help others to use"""
    return Response(
        markdown2.markdown(open("README.md", 'r').read()),
        mimetype='text/html')


blueprint = Blueprint('LEFT', __name__)
api.init_app(blueprint)
api.add_namespace(hashtags_namespace)
api.add_namespace(users_namespace)
application.register_blueprint(blueprint)

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    api_key = os.environ.get('TWITTER_API_KEY')
    api_secret_key = os.environ.get('TWITTER_API_SECRET_KEYS')

    try:
        TwitterRequests(api_key, api_secret_key)
    except TwitterKeyAbsentError:
        print("please put set twitter api keys as environ varables, "
              "TWITTER_API_KEY, TWITTER_API_SECRET_KEYS")
        sys.exit(1)

    print("Listen Everything From Tweets (LEFT) on {}".format(port))
    application.run(host='0.0.0.0', port=port)
