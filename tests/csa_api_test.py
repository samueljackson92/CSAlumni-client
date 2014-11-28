from csa_api import CsaAPI, constants

import unittest
import nose.tools
import requests
import responses
from test_helpers import load_fixture

class ApiTests(unittest.TestCase):

    def setUp(self):
        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/verify'),
                      body="{\"id\": 41}",
                      status=200,
                      content_type='application/json')

        self._default_user_name = "admin"
        self._default_password = "taliesin"

    @responses.activate
    def test_create_api_handle(self):
        api = CsaAPI(self._default_user_name, self._default_password)
        nose.tools.assert_is_not_none(api)

    @responses.activate
    def test_build_end_point_uri(self):
        constants.PROTOCOL = 'http://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3000'
        constants.CONTENT_TYPE = 'json'

        api = CsaAPI(self._default_user_name, self._default_password)
        uri = api._build_end_point_uri("/home/index")
        nose.tools.assert_equal('http://localhost:3000/home/index.json', uri)

    @nose.tools.raises(KeyError)
    def test_build_invalid_end_point_uri(self):
        constants.PROTOCOL = 'http://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3000'
        constants.CONTENT_TYPE = 'json'

        uri = CsaAPI._build_end_point_uri("/home/index")

    @responses.activate
    def test_build_end_point_uri_with_vars(self):
        constants.PROTOCOL = 'http://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3000'
        constants.CONTENT_TYPE = 'json'

        api = CsaAPI(self._default_user_name, self._default_password)
        uri = api._build_end_point_uri("/users/show/:id", params={':id': '42'})
        nose.tools.assert_equal('http://localhost:3000/users/show/42.json', uri)

    @nose.tools.raises(ValueError)
    def test_build_end_point_uri_with_vars_and_no_params(self):
        constants.PROTOCOL = 'http://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3000'
        constants.CONTENT_TYPE = 'json'

        uri = CsaAPI._build_end_point_uri("/users/show/:id", params={})

    @responses.activate
    def test_build_end_point_uri_with_no_vars_and_params(self):
        # This should pass becuase the supplied parameters are ignored.
        constants.PROTOCOL = 'http://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3000'
        constants.CONTENT_TYPE = 'json'

        api = CsaAPI(self._default_user_name, self._default_password)
        uri = api._build_end_point_uri("/users/search", params={':id': '42'})
        nose.tools.assert_equal('http://localhost:3000/users/search.json', uri)

    @responses.activate
    def test_build_end_point_uri_with_numeric_param(self):
        # This should pass becuase the supplied parameters are ignored.
        constants.PROTOCOL = 'http://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3000'
        constants.CONTENT_TYPE = 'json'


        api = CsaAPI(self._default_user_name, self._default_password)
        uri = api._build_end_point_uri("/users/search", params={':id': 42})
        nose.tools.assert_equal('http://localhost:3000/users/search.json', uri)

    @responses.activate
    def test_build_end_point_uri(self):
        constants.PROTOCOL = 'http://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3000'

        api = CsaAPI(self._default_user_name, self._default_password)
        uri = api._build_domain_address()
        nose.tools.assert_equal('http://localhost:3000', uri)

    @responses.activate
    def test_connect_with_HTTP_auth(self):

        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/show/:id',
                                                    {':id': '41'}),
                      body=load_fixture('users/show/41.json'),
                      status=200,
                      content_type='application/json')

        api = CsaAPI("admin", "taliesin")
        resp = api.make_request("/users/show/:id", {':id':'41'})
        nose.tools.assert_equal("Loftus", resp["surname"])

    @responses.activate
    @nose.tools.raises(requests.exceptions.HTTPError)
    def test_fail_to_connect_with_HTTP_auth(self):
        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/show/:id',
                                                    {':id': '41'}),
                      body='',
                      status=403,
                      content_type='application/json')

        #connect using an invalid password
        api = CsaAPI("admin", "not_a_password")
        resp = api.make_request("/users/show/:id", {':id':'41'})


    @responses.activate
    def test_request_can_view_user(self):
        responses.reset()
        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/verify'),
                      body="{\"id\": 39}",
                      status=200,
                      content_type='application/json')

        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/show/:id',
                                                    {':id': '39'}),
                      body=load_fixture('users/show/39.json'),
                      status=200,
                      content_type='application/json')

        api = CsaAPI("cwl39", 'taliesin')
        resp = api.get_user()

        nose.tools.assert_equal("Firstname39", resp["firstname"])
        nose.tools.assert_equal("Surname39", resp["surname"])
        nose.tools.assert_equal(1985, resp["grad_year"])
        nose.tools.assert_equal("01970 622422", resp["phone"])
        nose.tools.assert_equal("cwl39@aber.ac.uk", resp["email"])
        nose.tools.assert_equal(True, resp["jobs"])
        nose.tools.assert_equal("2013-09-04T13:51:00.311Z", resp["created_at"])
        nose.tools.assert_equal("2013-09-04T13:51:00.311Z", resp["updated_at"])

    @responses.activate
    @nose.tools.raises(requests.exceptions.HTTPError)
    def test_request_cannot_view_other_user(self):
        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/show/:id',
                                                    {':id': '41'}),
                      body='',
                      status=403,
                      content_type='application/json')

        api = CsaAPI("cwl39", 'taliesin')
        resp = api.get_user('41')

    @responses.activate
    def test_request_admin_can_view_user(self):
        responses.reset()
        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/verify'),
                      body="{\"id\": 39}",
                      status=200,
                      content_type='application/json')

        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/show/:id',
                                                    {':id': '39'}),
                      body=load_fixture('users/show/39.json'),
                      status=200,
                      content_type='application/json')

        api = CsaAPI("admin", 'taliesin')
        resp = api.get_user('39')

        nose.tools.assert_equal("Firstname39", resp["firstname"])
        nose.tools.assert_equal("Surname39", resp["surname"])
        nose.tools.assert_equal(1985, resp["grad_year"])
        nose.tools.assert_equal("01970 622422", resp["phone"])
        nose.tools.assert_equal("cwl39@aber.ac.uk", resp["email"])
        nose.tools.assert_equal(True, resp["jobs"])
        nose.tools.assert_equal("2013-09-04T13:51:00.311Z", resp["created_at"])
        nose.tools.assert_equal("2013-09-04T13:51:00.311Z", resp["updated_at"])
