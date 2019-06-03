import base64
from functools import lru_cache
import json
import logging
from urllib.parse import urlencode

import requests

logger = logging.getLogger(__name__)

class TwitterConnectionError(Exception):
    """Unable to connect Twitter API server"""
    pass

class TwitterFormatError(Exception):
    """Unexpect format from Twitter"""
    pass

class TwitterAPICredentialError(Exception):
    """Credential of Twitter Error"""
    pass


class TwitterRequests():
    """a request warpper for twitter"""

    __slots__ = ("_token",)

    __instance = None  # regist by API key

    def __new__(cls, token=None, api_key=None, api_secret_key=None):
        if TwitterRequests.__instance:
            return TwitterRequests.__instance
        return object.__new__(cls)

    def __init__(self, token=None, api_key=None, api_secret_key=None):
        if not TwitterRequests.__instance:
            if token:
                self._token = token
            elif api_key and api_secret_key:
                self._token = self.login(api_key, api_secret_key)
            else:
                raise TwitterAPICredentialError('Lack of API keys or token')

            TwitterRequests.__instance = self

    def __del__(self):
        del TwitterRequests.__instance

    def login(self, api_key, api_secret_key):
        try:
            auth = base64.b64encode(
                "{}:{}".format(api_key, api_secret_key).encode('utf-8')
            ).decode('utf-8')
            r = requests.post(
                'https://api.twitter.com/oauth2/token',
                data={'grant_type': 'client_credentials'},
                headers={
                    'Authorization': 'Basic {}=='.format(auth),
                    'Content-type': 'application/x-www-form-urlencoded;charset=UTF-8'
                })
            return json.loads(r.text)['access_token']
        except:
            logger.exception("Twitter login fail")
            raise TwitterAPICredentialError('Twitter login fail')

    def _raw_query(self, uri, **kwarg):
        for _ in range(3):
            try:
                url = "https://api.twitter.com/1.1{}?{}".format(uri, urlencode(kwarg))
                r = requests.get(url, headers={"Authorization": "Bearer " + self._token})
                if r.status_code == 401:
                    logger.error(f"Twitter Token Deny: {r.text}")
                    raise TwitterAPICredentialError("Twitter Token Deny")

                if r.status_code == 200:
                    logger.debug(f"{url} [200] {r.text}")
                    return r.text
                else:
                    logger.info(r.status_code)
                    logger.info(r.text)
            except:
                logger.warning(f"{uri} [{getattr(r, 'status_code', '')}] "
                               f"{getattr(r, 'text', '')}")

        logger.error(f"query {uri} fail : {kwarg}")
        raise TwitterConnectionError()

    @lru_cache(maxsize=128)
    def standard_query(self, query_str, count=30):
        try:
            return json.loads(
                self._raw_query("/search/tweets.json", q=query_str, count=count))['statuses']
        except TwitterConnectionError as e:
            raise e
        except:
            logger.exception("standard query return format error")
            raise TwitterFormatError()

    @lru_cache(maxsize=128)
    def user_timeline(self, user, count=30):
        try:
            return json.loads(self._raw_query("/statuses/user_timeline.json", screen_name=user, count=count))
        except TwitterConnectionError as e:
            raise e
        except:
            logger.exception("user timeline return format error")
            raise TwitterFormatError()
