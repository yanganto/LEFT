import json
import os
import signal
import subprocess
from time import sleep

import pytest
import requests


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

