import unittest
import nose.tools
import requests
import responses
import json

from requests.exceptions import HTTPError
from test_helpers import *
from csa_client import constants
from csa_client.oauth import OAuth2ResourceOwner, OAuth2Tokens

class OAuth2ResourceOwnerTest(unittest.TestCase):

    def setUp(self):
        self.oauth_handler = OAuth2ResourceOwner('/oauth/token')

    @responses.activate
    def test_init_object(self):
        oauth_handler = OAuth2ResourceOwner('/oauth/token')

    @responses.activate
    def test_request_auth_client_credentails(self):
        url = "https://localhost:3001/oauth/token.json"
        expected_payload = {'grant_type': 'password', 'username': 'admin', 'password': 'password'}
        resp_body = {'access_token': 'abcd', 'refresh_token': 'abcd'}

        def check_payload(request):
            body = json.loads(request.body)
            nose.tools.assert_dict_equal(expected_payload, body)

            return (200, {}, json.dumps(resp_body))

        responses.add_callback(responses.POST, url, callback=check_payload)
        self.oauth_handler.request_auth_with_client_credentials('admin', 'password')
        tokens = self.oauth_handler.get_tokens()
        nose.tools.assert_dict_equal(resp_body, tokens)

    @responses.activate
    @nose.tools.raises(HTTPError)
    def test_request_auth_client_credentails_fails(self):
        url = "https://localhost:3001/oauth/token.json"
        expected_payload = {'grant_type': 'password', 'username': 'admin', 'password': 'password'}

        def check_payload(request):
            body = json.loads(request.body)
            nose.tools.assert_dict_equal(expected_payload, body)
            return (401, {}, {'error': 'some error message'})

        responses.add_callback(responses.POST, url, callback=check_payload)
        self.oauth_handler.request_auth_with_client_credentials('admin', 'password')

    @responses.activate
    def test_request_auth_with_refresh_tokens(self):
        url = "https://localhost:3001/oauth/token.json"
        expected_payload = {'access_token': 'abcd', 'grant_type': 'refresh_token', 'refresh_token': 'abcd'}
        orig_tokens = {'access_token': 'abcd', 'refresh_token': 'abcd'}
        resp_body = {'access_token': 'new_tokens', 'refresh_token': 'new_tokens'}

        def check_payload(request):
            body = json.loads(request.body)
            nose.tools.assert_dict_equal(expected_payload, body)
            return (200, {}, json.dumps(resp_body))

        responses.add_callback(responses.POST, url, callback=check_payload)

        self.oauth_handler.set_tokens(orig_tokens)
        self.oauth_handler.request_auth_with_refresh_token()
        tokens = self.oauth_handler.get_tokens()
        nose.tools.assert_dict_equal(resp_body, tokens)

class OAuth2TokensTest(unittest.TestCase):

    def setUp(self):
        self.oauth_tokens = OAuth2Tokens('abcd')

    def test_oauth_appends_token(self):
        class request:
            def __init__(self, d):
                self.body = d

        r = request(json.dumps({'some': 'data'}))
        response = self.oauth_tokens(r)
        nose.tools.assert_equal('{"access_token": "abcd", "some": "data"}', response.body)
