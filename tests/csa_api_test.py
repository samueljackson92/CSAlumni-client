from csa_api import CsaAPI, constants

import unittest
import nose.tools
import requests
import responses
from test_helpers import load_fixture

class ApiTests(unittest.TestCase):
    def setUp(self):
        user_name = "my_user_name"
        password = "my_password"
        self.api = CsaAPI(user_name, password)

    def test_create_api_handle(self):
        nose.tools.assert_is_not_none(self.api)

    def test_build_end_point_uri(self):
        constants.PROTOCOL = 'http://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3000'
        constants.CONTENT_TYPE = 'json'

        uri = self.api._build_end_point_uri("/home/index")
        nose.tools.assert_equal('http://localhost:3000/home/index.json', uri)

    @nose.tools.raises(KeyError)
    def test_build_invalid_end_point_uri(self):
        constants.PROTOCOL = 'http://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3000'
        constants.CONTENT_TYPE = 'json'

        uri = self.api._build_end_point_uri("/home/index")

    def test_build_end_point_uri_with_vars(self):
        constants.PROTOCOL = 'http://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3000'
        constants.CONTENT_TYPE = 'json'

        uri = self.api._build_end_point_uri("/users/show/:id", params={':id': '42'})
        nose.tools.assert_equal('http://localhost:3000/users/show/42.json', uri)

    @nose.tools.raises(ValueError)
    def test_build_end_point_uri_with_vars_and_no_params(self):
        constants.PROTOCOL = 'http://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3000'
        constants.CONTENT_TYPE = 'json'

        uri = self.api._build_end_point_uri("/users/show/:id", params={})

    def test_build_end_point_uri_with_no_vars_and_params(self):
        # This should pass becuase the supplied parameters are ignored.
        constants.PROTOCOL = 'http://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3000'
        constants.CONTENT_TYPE = 'json'

        uri = self.api._build_end_point_uri("/users/search", params={':id': '42'})
        nose.tools.assert_equal('http://localhost:3000/users/search.json', uri)

    def test_build_end_point_uri_with_numeric_param(self):
        # This should pass becuase the supplied parameters are ignored.
        constants.PROTOCOL = 'http://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3000'
        constants.CONTENT_TYPE = 'json'

        uri = self.api._build_end_point_uri("/users/search", params={':id': 42})
        nose.tools.assert_equal('http://localhost:3000/users/search.json', uri)

    def test_build_end_point_uri(self):
        constants.PROTOCOL = 'http://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3000'

        uri = self.api._build_domain_address()
        nose.tools.assert_equal('http://localhost:3000', uri)

    @responses.activate
    def test_connect_with_HTTP_auth(self):
        responses.add(responses.GET,
                      self.api._build_end_point_uri('/users/show/:id',
                                                    {':id': '41'}),
                      body=load_fixture('users/show/41.json'),
                      status=200,
                      content_type='application/json')

        self.api = CsaAPI("admin", "taliesin")
        resp = self.api.make_request("/users/show/:id", {':id':'41'})
        nose.tools.assert_equal("Loftus", resp["surname"])

    @responses.activate
    @nose.tools.raises(requests.exceptions.HTTPError)
    def test_fail_to_connect_with_HTTP_auth(self):
        responses.add(responses.GET,
                      self.api._build_end_point_uri('/users/show/:id',
                                                    {':id': '41'}),
                      body='',
                      status=403,
                      content_type='application/json')

        #connect using an invalid password
        self.api = CsaAPI("admin", "not_a_password")
        resp = self.api.make_request("/users/show/:id", {':id':'41'})

