import json
import os
import signal
import subprocess
from time import sleep

import requests


class TestLEFT(object):
    """API Test for LEFT Server"""
    left_server = None

    @classmethod
    def setup_class(cls):
        """run LEFT server"""
        cls.left_server = subprocess.Popen('python3 main.py', shell=True)
        sleep(3)


    @classmethod
    def teardown_class(cls):
        """stop LEFT server"""
        os.kill(cls.left_server.pid, signal.SIGTERM)

    def test_query_by_hashtags(self):
        r = requests.get('http://127.0.0.1:8080/hashtags', headers={"accept": "application/json"})
        assert json.loads(r.text) == []

    def test_query_by_users(self):
        r = requests.get('http://127.0.0.1:8080/users', headers={"accept": "application/json"})
        assert json.loads(r.text) == []
