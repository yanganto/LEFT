import json
import os
import signal
import subprocess
from time import sleep

import pytest
import requests

from api.model import status_formator, _time_string_formator

@pytest.mark.skipif(
    not os.environ.get("TWITTER_TOKEN"),
    reason="Lack twitter token to run test")
class TestLEFTAPI():
    """API Test for LEFT Server"""
    left_server = None

    @classmethod
    def setup_class(cls):
        """run LEFT server"""
        cls.left_server = subprocess.Popen('python3 left.py', shell=True)
        sleep(3)


    @classmethod
    def teardown_class(cls):
        """stop LEFT server"""
        os.kill(cls.left_server.pid, signal.SIGTERM)

    def test_query_by_hashtags(self):
        r = requests.get('http://127.0.0.1:8080/hashtags/python?limit=1',
                         headers={"accept": "application/json"})
        assert len(json.loads(r.text)) == 1

    def test_query_by_users(self):
        r = requests.get('http://127.0.0.1:8080/users/twitter?limit=1',
                         headers={"accept": "application/json"})
        assert len(json.loads(r.text)) == 1

class TestLEFTModel():
    def test_status_formator(self):
        status = {"created_at": "Mon Jan 02 06:33:20 +0000 2017",
                  "id": 815808174183759900,
                  "id_str": "815808174183759873",
                  "text": "...",
                  "truncated": False,
                  "entities": {"hashtags": [],
                               "symbols": [],
                               "user_mentions": [],
                               "urls": []},
                  "source": "<a href=\"http://twitter.com/download/android\" rel=\"nofollow\">Twitter for Android</a>",
                  "in_reply_to_status_id": None,
                  "in_reply_to_status_id_str": None,
                  "in_reply_to_user_id": None,
                  "in_reply_to_user_id_str": None,
                  "in_reply_to_screen_name": None,
                  "user": {"id": 555234030,
                           "id_str": "555234030",
                           "name": "Antonio Yang",
                           "screen_name": "__yanganto__",
                           "location": "Taipei, Taiwan",
                           "description": "",
                           "url": None,
                           "entities": {"description": {"urls": []}},
                           "protected": False,
                           "followers_count": 5,
                           "friends_count": 8,
                           "listed_count": 0,
                           "created_at": "Mon Apr 16 14:10:11 +0000 2012",
                           "favourites_count": 0,
                           "utc_offset": None,
                           "time_zone": None,
                           "geo_enabled": True,
                           "verified": False,
                           "statuses_count": 50,
                           "lang": None,
                           "contributors_enabled": False,
                           "is_translator": False,
                           "is_translation_enabled": False,
                           "profile_background_color": "000000",
                           "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png",
                           "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png",
                           "profile_background_tile": False,
                           "profile_image_url": "http://pbs.twimg.com/profile_images/418755000265756674/L99DSXq1_normal.jpeg",
                           "profile_image_url_https": "https://pbs.twimg.com/profile_images/418755000265756674/L99DSXq1_normal.jpeg",
                           "profile_link_color": "91D2FA",
                           "profile_sidebar_border_color": "000000",
                           "profile_sidebar_fill_color": "000000",
                           "profile_text_color": "000000",
                           "profile_use_background_image": False,
                           "has_extended_profile": False,
                           "default_profile": False,
                           "default_profile_image": False,
                           "following": None,
                           "follow_request_sent": None,
                           "notifications": None,
                           "translator_type": "none"},
                  "geo": None,
                  "coordinates": None,
                  "place": None,
                  "contributors": None,
                  "is_quote_status": False,
                  "retweet_count": 0,
                  "favorite_count": 0,
                  "favorited": False,
                  "retweeted": False,
                  "lang": "ja"}
        assert status_formator(status) == {'account': {'fullname': 'Antonio Yang',
                                                       'href': '/__yanganto__',
                                                       'id': 555234030},
                                           'date': '6:33 AM - 2 Jan 2017',
                                           'hashtags': [],
                                           'likes': 0,
                                           'retweets': 0,
                                           'text': '...'}


    def test_time_formator(self):
        assert _time_string_formator("Fri Mar 08 14:54:01 +0000 2018") == "2:54 PM - 8 Mar 2018"


class TestLEFTCli():
    def teardown_method(self, method):
        """stop LEFT server"""
        os.kill(self.left_server.pid, signal.SIGTERM)
        if os.path.isfile('/tmp/left.log'):
            os.remove('/tmp/left.log')


    def test_set_up_log_fil(self):
        self.left_server = subprocess.Popen('python3 left.py -l /tmp/left.log', shell=True)
        sleep(3)
        assert os.path.isfile('/tmp/left.log')
