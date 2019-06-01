from utils.twitter_requests import TwitterRequests, _time_string_formator

class TestTwitterRequests():
    def test_twitter_request_sigleton(self):
        r1 = TwitterRequests('api_key', 'api_secret_key')
        r2 = TwitterRequests('api_key', 'api_secret_key')
        assert id(r1) == id(r2)

    def test_time_formator(self):
        assert _time_string_formator("Fri Mar 08 14:54:01 +0000 2018") == "2:54 PM - 8 Mar 2018"
