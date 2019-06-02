"""LEFT
usage: left.py [-h] [-v] [-k API_KEY] [-s API_SECRET_KEY] [-t TOKEN] [-p PORT]

optional arguments:
  -k API_KEY, --key=API_KEY
    if TOEKEN is not provided, API_KEY and API_SECRET_KEY should provided to obtain then token.

  -h, --help
    show this help message and exit

  -s API_SECRET_KEY, --secret=API_SECRET_KEY
    if TOEKEN is not provided, API_KEY and API_SECRET_KEY should provided to obtain then token.

  -t TOKEN, --token=TOKEN
    The TOKEN is the credential to access Twiter API server.

  -p PORT, --port=PORT
    The port service run on.

  -v, --verbos
    Change the logging level to DEBUG
"""
import logging
import os
import sys

from flask import Flask, Blueprint, Response
import markdown2

from api import api
from api.hashtags import ns as hashtags_namespace
from api.users import ns as users_namespace
from utils.twitter_requests import TwitterRequests, TwitterAPICredentialError

logger = logging.getLogger('left')

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
    import getopt
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "k:s:t:p:vh",
                                   ['key', 'secret', 'token', 'port', 'verbose', 'help'])
    except getopt.GetoptError as e:
        print(__doc__)
        sys.exit("invalid option: " + str(e))

    port = 8080
    api_key = None
    api_secret_key = None
    api_token = None
    logger_level = logging.INFO

    try:
        for o, a in opts:
            if o in ('-h', '--help'):
                print(__doc__)
                sys.exit(0)
            elif o in ('-p', '--port'):
                port = int(a)
            elif o in ('-k', '--key'):
                api_key = a
            elif o in ('-s', '--secret'):
                api_secret_key = a
            elif o in ('-t', '--token'):
                token = a
            elif o in ('-v', '--verbose'):
                logger_level = logging.DEBUG  # INFO or DEBUG, just simple

    except ValueError:
        sys.exit("invalid value of option {}: {}".format(o, a))
    except:
        sys.exit("invalid options " + o)
        print(__doc__)

    logging.basicConfig(filename="left.log", level=logger_level,
                        format='%(levelname)s:%(name)s:%(message)s')
    if not api_token:
        api_token = os.environ.get('TWITTER_TOKEN')
        logger.debug("load TWITTER_TOKEN from environment")

    logger.debug(f'port: {port}')
    logger.debug(f'api_key: {api_key}')
    logger.debug(f'api_secret_key: {api_secret_key}')
    logger.debug(f'api_token: {api_token}')

    try:
        TwitterRequests(api_token, api_key, api_secret_key)
    except TwitterAPICredentialError:
        sys.exit("please set up twitter api credentails as one of following way:\n"
                 "1. set token as environ varables (TWITTER_TOKEN)\n"
                 "2. provide token in options (-t, --token)\n"
                 "3. provide api keys in options (-k, --key and -s, --secret)\n")

    print("Listen Everything From Tweets (LEFT) on {}".format(port))
    application.run(host='0.0.0.0', port=port)
