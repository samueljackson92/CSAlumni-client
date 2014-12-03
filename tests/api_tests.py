import unittest
import nose.tools
import requests
import responses
import json
import os

from requests.exceptions import HTTPError
from test_helpers import *
from csa_client import constants
from csa_client.api import CsaAPI

class ApiTests(unittest.TestCase):

    def tearDown(self):
        responses.reset()
        if os.path.isfile(constants.TOKEN_FILE):
            os.remove(constants.TOKEN_FILE)

    @responses.activate
    def test_build_end_point_uri(self):
        constants.PROTOCOL = 'https://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3001'
        constants.CONTENT_TYPE = 'json'

        uri = RequestHandler._build_end_point_uri("/home/index")
        nose.tools.assert_equal('https://localhost:3001/home/index.json', uri)

    @nose.tools.raises(KeyError)
    def test_build_invalid_end_point_uri(self):
        constants.PROTOCOL = 'https://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3001'
        constants.CONTENT_TYPE = 'json'

        uri = RequestHandler._build_end_point_uri("/home/index")

    @responses.activate
    def test_build_end_point_uri_with_vars(self):
        constants.PROTOCOL = 'https://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3001'
        constants.CONTENT_TYPE = 'json'

        uri = RequestHandler._build_end_point_uri("/users/show/:id", params={':id': '42'})
        nose.tools.assert_equal('https://localhost:3001/users/show/42.json', uri)

    @nose.tools.raises(ValueError)
    def test_build_end_point_uri_with_vars_and_no_params(self):
        constants.PROTOCOL = 'https://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3001'
        constants.CONTENT_TYPE = 'json'

        uri = RequestHandler._build_end_point_uri("/users/show/:id", params={})

    @responses.activate
    def test_build_end_point_uri_with_no_vars_and_params(self):
        # This should pass becuase the supplied parameters are ignored.
        constants.PROTOCOL = 'https://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3001'
        constants.CONTENT_TYPE = 'json'

        uri = RequestHandler._build_end_point_uri("/users/search", params={':id': '42'})
        nose.tools.assert_equal('https://localhost:3001/users/search.json', uri)

    @responses.activate
    def test_build_end_point_uri_with_numeric_param(self):
        # This should pass becuase the supplied parameters are ignored.
        constants.PROTOCOL = 'https://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3001'
        constants.CONTENT_TYPE = 'json'

        uri = RequestHandler._build_end_point_uri("/users/search", params={':id': 42})
        nose.tools.assert_equal('https://localhost:3001/users/search.json', uri)

    @responses.activate
    def test_build_end_point_uri(self):
        constants.PROTOCOL = 'https://'
        constants.DOMAIN = 'localhost'
        constants.PORT = '3001'

        uri = RequestHandler._build_domain_address()
        nose.tools.assert_equal('https://localhost:3001', uri)

    ##########################################################################
    # User tests
    ##########################################################################

    @responses.activate
    def test_create_user(self):
        responses.reset()

        fixture = load_fixture("users/show/39.json")
        fixture = json.loads(fixture)
        def check_user_was_created(request):
            body = json.loads(request.body)
            fixture.update({'access_token': body['access_token']})
            nose.tools.assert_equal(fixture, body)
            return (200, {}, {})


        mock_auth_response()

        responses.add_callback(responses.POST,
                      RequestHandler._build_end_point_uri('/users/create'),
                      callback=check_user_was_created,
                      content_type='application/json')

        api = CsaAPI("admin", 'taliesin')
        api.create_user(fixture)

    @responses.activate
    def test_request_can_view_user(self):
        mock_auth_response()
        fixture = mock_show_user_response(39)

        api = CsaAPI("cwl39", 'taliesin')
        resp = api.get_user(39)

        nose.tools.assert_dict_equal(fixture, resp)

    @responses.activate
    @nose.tools.raises(requests.exceptions.HTTPError)
    def test_request_cannot_view_other_user(self):
        mock_auth_response()
        mock_show_user_response(41, status=403)

        api = CsaAPI("cwl39", 'taliesin')
        resp = api.get_user(41)

    @responses.activate
    def test_request_admin_can_view_user(self):
        mock_auth_response()
        fixture = mock_show_user_response(39)

        api = CsaAPI("admin", 'taliesin')
        resp = api.get_user(39)

        nose.tools.assert_dict_equal(fixture, resp)

    @responses.activate
    def test_user_can_update_self(self):
        # Mock requests for auth, get user
        mock_auth_response()
        fixture = mock_show_user_response(39)

        # Mock update request to modify the fixture
        def check_payload(request):
            payload = json.loads(request.body)
            nose.tools.assert_equal(1986, payload["grad_year"])
            fixture['grad_year'] = payload["grad_year"]
            return (200, {}, {})

        responses.add_callback(responses.PUT,
                      RequestHandler._build_end_point_uri('/users/update/:id',
                                                    {':id': '39'}),
                      callback=check_payload,
                      content_type='application/json')


        # Get the user and make some changes
        api = CsaAPI("cwl39", 'taliesin')
        user = api.get_user(39)
        user["grad_year"] = 1986
        api.update_user(user)

        # Mock the updated user response
        responses.reset()
        mock_show_user_response(39, body=json.dumps(fixture))

        # Check it matches
        resp = api.get_user(39)
        nose.tools.assert_equal(1986, resp["grad_year"])

    @responses.activate
    @nose.tools.raises(requests.exceptions.HTTPError)
    def test_user_cannot_update_other_user(self):
        mock_auth_response()
        mock_show_user_response(41)

        responses.add(responses.PUT,
                      RequestHandler._build_end_point_uri('/users/update/:id',
                                                    {':id': '41'}),
                      status=422,
                      content_type='application/json')

        api = CsaAPI("cwl39", 'taliesin')
        user = api.get_user(41)
        user["grad_year"] = 1986
        api.update_user(user)

    @responses.activate
    def test_admin_can_update_other_user(self):
        mock_auth_response()
        fixture = mock_show_user_response(39)

        # Mock update request to modify the fixture
        def check_payload(request):
            payload = json.loads(request.body)
            fixture["grad_year"] = payload["grad_year"]
            nose.tools.assert_equal(1986, payload["grad_year"])
            return (200, {}, {})

        responses.add_callback(responses.PUT,
                      RequestHandler._build_end_point_uri('/users/update/:id',
                                                    {':id': '39'}),
                      callback=check_payload,
                      content_type='application/json')


        # Get the user and make some changes
        api = CsaAPI("admin", 'taliesin')
        user = api.get_user(39)
        user["grad_year"] = 1986
        api.update_user(user)

        # Mock the updated user response
        responses.reset()
        mock_show_user_response(39, body=json.dumps(fixture))

        # Check it matches
        resp = api.get_user(39)
        nose.tools.assert_equal(1986, resp["grad_year"])


    @responses.activate
    @nose.tools.raises(requests.exceptions.HTTPError)
    def test_user_cannot_destroy(self):
        mock_auth_response()

        responses.add(responses.DELETE,
                      RequestHandler._build_end_point_uri('/users/destory/:id',
                                                    {':id': '39'}),
                      status=422,
                      content_type='application/json')

        api = CsaAPI("cwl39", 'taliesin')
        api.destroy_user(39)

    @responses.activate
    def test_admin_can_destory(self):
        mock_auth_response()

        responses.add(responses.DELETE,
                      RequestHandler._build_end_point_uri('/users/destory/:id',
                                                    {':id': '39'}),
                      status=200,
                      content_type='application/json')

        api = CsaAPI("admin", 'taliesin')
        api.destroy_user(39)

    @responses.activate
    def test_user_search_no_query(self):
        mock_auth_response()

        search_fixture = json.loads(load_fixture('users/search.json'))
        responses.add(responses.GET,
                      RequestHandler._build_end_point_uri('/users/search'),
                      body=json.dumps(search_fixture),
                      status=200,
                      content_type='application/json')

        api = CsaAPI("admin", 'taliesin')
        response = api.search()

        nose.tools.assert_list_equal(search_fixture, response)

    @responses.activate
    def test_user_search_with_query(self):
        mock_auth_response()

        search_fixture = json.loads(load_fixture('users/search.json'))
        search_fixture = search_fixture[:1]
        responses.add(responses.GET,
                      RequestHandler._build_end_point_uri('/users/search'),
                      body=json.dumps(search_fixture),
                      status=200,
                      content_type='application/json')

        api = CsaAPI("admin", 'taliesin')
        response = api.search()
        nose.tools.assert_list_equal(search_fixture, response)

    @responses.activate
    @nose.tools.raises(requests.exceptions.HTTPError)
    def test_user_cannot_search(self):
        mock_auth_response()

        responses.add(responses.GET,
                      RequestHandler._build_end_point_uri('/users/search'),
                      status=422,
                      content_type='application/json')

        api = CsaAPI("cwl39", 'taliesin')
        response = api.search()


    ##########################################################################
    # Broadcast tests
    ##########################################################################

    @responses.activate
    def test_create_broadcast(self):
        mock_auth_response()

        fixture = load_fixture("broadcasts/1.json")
        fixture = json.loads(fixture)

        def check_broadcast_was_created(request):
            body = json.loads(request.body)
            fixture.update({'access_token': body['access_token']})
            nose.tools.assert_dict_equal(fixture, body)
            return (200, {}, {})

        responses.add_callback(responses.POST,
                      RequestHandler._build_end_point_uri('/broadcasts/create'),
                      callback=check_broadcast_was_created,
                      content_type='application/json')

        api = CsaAPI("admin", 'taliesin')
        api.create_broadcast(fixture)

    @responses.activate
    def test_get_broadcast(self):
        mock_auth_response()

        fixture = load_fixture("broadcasts/1.json")
        responses.add(responses.GET,
                      RequestHandler._build_end_point_uri('/broadcasts/show/:id',
                                                 {':id': '1'}),
                      body=fixture,
                      status=200,
                      content_type='application/json')

        api = CsaAPI("admin", 'taliesin')
        broadcast = api.get_broadcast(1)
        nose.tools.assert_dict_equal(json.loads(fixture), broadcast)

    @responses.activate
    def test_destory_broadcast(self):
        mock_auth_response()

        def assert_delete(request):
            nose.tools.assert_equal(responses.DELETE, request.method)
            return (200, {}, {})

        fixture = load_fixture("broadcasts/1.json")
        responses.add_callback(responses.DELETE,
                      RequestHandler._build_end_point_uri('/broadcasts/destroy/:id',
                                                 {':id': '1'}),
                      callback=assert_delete,
                      content_type='application/json')

        api = CsaAPI("admin", 'taliesin')
        broadcast = api.destroy_broadcast(1)

    @responses.activate
    def test_get_broadcasts(self):
        mock_auth_response()

        fixture = load_fixture("broadcasts.json")
        responses.add(responses.GET,
                      RequestHandler._build_end_point_uri('/broadcasts'),
                      body=fixture,
                      status=200,
                      content_type='application/json')

        api = CsaAPI("admin", 'taliesin')
        broadcasts = api.get_broadcasts()
        nose.tools.assert_list_equal(json.loads(fixture), broadcasts)

    @responses.activate
    @nose.tools.raises(requests.exceptions.HTTPError)
    def test_make_coffee(self):
        mock_auth_response()

        responses.add('BREW',
                      RequestHandler._build_end_point_uri('/coffee'),
                      body=HTTPError('I\'m a teapot'),
                      status=418,
                      content_type='application/json')

        api = CsaAPI("admin", 'taliesin')
        response = api.make_coffee()