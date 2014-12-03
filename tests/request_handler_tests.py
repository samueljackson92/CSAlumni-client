import unittest
import nose.tools
import requests
import responses
import json

from requests.exceptions import HTTPError
from test_helpers import *
from csa_client import constants
from csa_client.request_handler import RequestHandler

class RequestHandlerTests(unittest.TestCase):

    def setUp(self):
        self.request_handler = RequestHandler()

    @responses.activate
    def test_make_request(self):
        url = "https://localhost:3001/users/create.json"
        responses.add(responses.POST, url)
        self.request_handler.make_request('/users/create')

    @responses.activate
    def test_make_request_with_end_point_vars(self):
        url = "https://localhost:3001/users/show/41.json"
        responses.add(responses.GET, url)
        self.request_handler.make_request('/users/show/:id', {':id': '41'})

    @responses.activate
    def test_make_request_with_params(self):
        url = "https://localhost:3001/users/create.json"
        test_params = {'some': 'data'}

        def check_payload(request):
            body = json.loads(request.body)
            nose.tools.assert_equal(test_params, body)
            return (200, {}, {})

        responses.add_callback(responses.POST, url, callback=check_payload)
        self.request_handler.make_request('/users/create', params=test_params)

    def test_build_end_point_uri(self):
        constants.PROTOCOL = 'https://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3001'
        constants.CONTENT_TYPE = 'json'

        uri = self.request_handler._build_end_point_uri("/home/index")
        nose.tools.assert_equal('https://localhost:3001/home/index.json', uri)

    @nose.tools.raises(KeyError)
    def test_build_invalid_end_point_uri(self):
        constants.PROTOCOL = 'https://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3001'
        constants.CONTENT_TYPE = 'json'

        uri = self.request_handler._build_end_point_uri("/home/index")

    def test_build_end_point_uri_with_vars(self):
        constants.PROTOCOL = 'https://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3001'
        constants.CONTENT_TYPE = 'json'

        uri = self.request_handler._build_end_point_uri("/users/show/:id", params={':id': '42'})
        nose.tools.assert_equal('https://localhost:3001/users/show/42.json', uri)

    @nose.tools.raises(ValueError)
    def test_build_end_point_uri_with_vars_and_no_params(self):
        constants.PROTOCOL = 'https://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3001'
        constants.CONTENT_TYPE = 'json'

        uri = self.request_handler._build_end_point_uri("/users/show/:id", params={})

    def test_build_end_point_uri_with_no_vars_and_params(self):
        # This should pass becuase the supplied parameters are ignored.
        constants.PROTOCOL = 'https://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3001'
        constants.CONTENT_TYPE = 'json'

        uri = self.request_handler._build_end_point_uri("/users/search", params={':id': '42'})
        nose.tools.assert_equal('https://localhost:3001/users/search.json', uri)

    def test_build_end_point_uri_with_numeric_param(self):
        # This should pass becuase the supplied parameters are ignored.
        constants.PROTOCOL = 'https://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3001'
        constants.CONTENT_TYPE = 'json'

        uri = self.request_handler._build_end_point_uri("/users/search", params={':id': 42})
        nose.tools.assert_equal('https://localhost:3001/users/search.json', uri)

    def test_build_end_point_uri(self):
        constants.PROTOCOL = 'https://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3001'

        uri = self.request_handler._build_domain_address()
        nose.tools.assert_equal('https://localhost:3001', uri)
