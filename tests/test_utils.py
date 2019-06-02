from utils.twitter_requests import TwitterRequests

class TestTwitterRequests():
    def test_twitter_request_sigleton(self):
        r1 = TwitterRequests('api_key', 'api_secret_key')
        r2 = TwitterRequests('api_key', 'api_secret_key')
        assert id(r1) == id(r2)
