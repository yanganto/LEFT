import sys

from flask import Flask, Blueprint, Response, request
from flask_restplus import Resource
import markdown2

from api import api
from api.hashtags import ns as hashtags_namespace
from api.users import ns as users_namespace

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
    print("Listen Everything From Tweets (LEFT) on {}".format(port))

    # Shutdown API for unit test
    @application.route('/shutdown')
    def shutdown():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
    application.run(host='0.0.0.0', port=port)
