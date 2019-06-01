import base64
from datetime import datetime
import json
from urllib.parse import urlencode

import requests


class TwitterConnectionError(Exception):
    """Unable to connect Twitter API server"""
    pass

class TwitterFormatError(Exception):
    """Unexpect format from Twitter"""
    pass

class TwitterKeyAbsentError(Exception):
    """Absent of Twitter API Keys"""
    pass


def _time_string_formator(orig):
    """from twitter time format to specific time format we want"""
    dt = datetime.strptime(orig, '%a %b %d %H:%M:%S +0000 %Y')
    return dt.strftime("%-I:%M %p - %-d %b %Y")


class TwitterRequests():
    """a request warpper for twitter"""

    __instance = None  # regist by API key

    def __new__(cls, api_key=None, api_secret_key=None):
        if TwitterRequests.__instance:
            return TwitterRequests.__instance
        return object.__new__(cls)

    def __init__(self, api_key=None, api_secret_key=None):
        if not TwitterRequests.__instance:

            if not api_key or not api_secret_key:
                raise TwitterKeyAbsentError()

            self.api_key = api_key
            self.token = self.login(api_secret_key)
            TwitterRequests.__instance = self

    def __del__(self):
        del TwitterRequests.__instance

    def login(self, api_secret_key):
        try:
            auth = base64.b64encode(
                "{}:{}".format(self.api_key, api_secret_key).encode('utf-8')
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
            RuntimeError("Twitter login fail")

    def _raw_query(self, query_str, count):
        for _ in range(3):
            try:
                r = requests.get(
                    "https://api.twitter.com/1.1/search/tweets.json?{}".format(
                        urlencode(dict(q=query_str, result_type="mixed", count=count))),
                    headers={"Authorization": "Bearer " + self.token})

                if r.status_code == 401:
                    # just prevent someone revoke the token unconsciously
                    self.login()
                    continue

                if r.status_code == 200:
                    return json.loads(r.text)
                else:
                    # TODO:
                    # redirect to log system or log file, depence on production environ
                    print(r.status_code)
                    print(r.text)
            except:
                pass
        raise TwitterConnectionError()

    def query(self, query_str, count=30):
        try:
            statuses = self._raw_query(query_str, count)['statuses']
            return [dict(
                    account={'id': s['user']['id'],
                             'fullname': s['user']['name'],
                             'href': '/' + s['user']['screen_name']},
                    date=_time_string_formator(s['created_at']),
                    text=s['text'],
                    hashtags=[t['text'] for t in s['entities'].get('hashtags', [])],
                    likes=s.get('favourites_count', 0),
                    retweets=s.get('retweet_count', 0)) for s in statuses]
        except TwitterConnectionError as e:
            raise e
        except:
            raise TwitterFormatError()
