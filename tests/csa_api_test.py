from csa_api import CsaAPI, constants

import unittest
import nose.tools
import requests
import responses
import json
from test_helpers import *

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
        json_response = resp.json()
        nose.tools.assert_equal("Loftus", json_response["surname"])

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

    ##########################################################################
    # User tests
    ##########################################################################

    @responses.activate
    def test_create_user(self):
        responses.reset()

        fixture = load_fixture("users/show/39.json")
        fixture = json.loads(fixture)
        def check_user_was_created(request):
            nose.tools.assert_equal(fixture, json.loads(request.body))
            return (200, {}, {})

        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/verify'),
                      body="{\"id\": 41}",
                      status=200,
                      content_type='application/json')

        responses.add_callback(responses.POST,
                      CsaAPI._build_end_point_uri('/users/create'),
                      callback=check_user_was_created,
                      content_type='application/json')

        api = CsaAPI("admin", 'taliesin')
        api.create_user(fixture)

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

    @responses.activate
    def test_user_can_update_self(self):
        responses.reset()

        def check_payload(request):
            payload = json.loads(request.body)
            nose.tools.assert_equal(1986, payload["grad_year"])
            return (200, {}, {})

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

        responses.add_callback(responses.PUT,
                      CsaAPI._build_end_point_uri('/users/update/:id',
                                                    {':id': '39'}),
                      callback=check_payload,
                      content_type='application/json')


        api = CsaAPI("cwl39", 'taliesin')
        user = api.get_user()
        user["grad_year"] = 1986
        api.update_user(user)

        responses.reset()
        fixture = json.loads(load_fixture('users/show/39.json'))
        fixture["grad_year"] = 1986
        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/show/:id',
                                                    {':id': '39'}),
                      body=json.dumps(fixture),
                      status=200,
                      content_type='application/json')


        resp = api.get_user()
        nose.tools.assert_equal(1986, resp["grad_year"])

    @responses.activate
    @nose.tools.raises(requests.exceptions.HTTPError)
    def test_user_cannot_update_other_user(self):
        responses.reset()
        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/verify'),
                      body="{\"id\": 39}",
                      status=200,
                      content_type='application/json')

        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/show/:id',
                                                    {':id': '41'}),
                      body=load_fixture('users/show/41.json'),
                      status=200,
                      content_type='application/json')

        responses.add(responses.PUT,
                      CsaAPI._build_end_point_uri('/users/update/:id',
                                                    {':id': '41'}),
                      status=422,
                      content_type='application/json')

        api = CsaAPI("cwl39", 'taliesin')
        user = api.get_user(41)
        user["grad_year"] = 1986
        api.update_user(user)

    @responses.activate
    def test_admin_can_update_other_user(self):
        responses.reset()

        def check_payload(request):
            payload = json.loads(request.body)
            nose.tools.assert_equal(1986, payload["grad_year"])
            return (200, {}, {})

        fixture = json.loads(load_fixture('users/show/39.json'))

        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/verify'),
                      body="{\"id\": 41}",
                      status=200,
                      content_type='application/json')

        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/show/:id',
                                                    {':id': '39'}),
                      body=load_fixture('users/show/39.json'),
                      status=200,
                      content_type='application/json')

        responses.add_callback(responses.PUT,
                      CsaAPI._build_end_point_uri('/users/update/:id',
                                                    {':id': '39'}),
                      callback=check_payload,
                      content_type='application/json')

        fixture = json.loads(load_fixture('users/show/39.json'))
        fixture["grad_year"] = 1986
        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/show/:id',
                                                    {':id': '39'}),
                      body=str(fixture),
                      status=200,
                      content_type='application/json')

        api = CsaAPI("cwl39", 'taliesin')
        user = api.get_user(39)
        user["grad_year"] = 1986
        api.update_user(user)

        responses.reset()
        fixture["grad_year"] = 1986
        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/show/:id',
                                                    {':id': '39'}),
                      body=json.dumps(fixture),
                      status=200,
                      content_type='application/json')

        resp = api.get_user(39)
        nose.tools.assert_equal(1986, resp["grad_year"])


    @responses.activate
    @nose.tools.raises(requests.exceptions.HTTPError)
    def test_user_cannot_destroy(self):
        responses.reset()
        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/verify'),
                      body="{\"id\": 39}",
                      status=200,
                      content_type='application/json')

        responses.add(responses.DELETE,
                      CsaAPI._build_end_point_uri('/users/destory/:id',
                                                    {':id': '39'}),
                      status=422,
                      content_type='application/json')

        api = CsaAPI("cwl39", 'taliesin')
        api.destory_user()

    @responses.activate
    def test_admin_can_destory(self):
        responses.reset()
        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/verify'),
                      body="{\"id\": 41}",
                      status=200,
                      content_type='application/json')

        responses.add(responses.DELETE,
                      CsaAPI._build_end_point_uri('/users/destory/:id',
                                                    {':id': '39'}),
                      status=200,
                      content_type='application/json')

        api = CsaAPI("admin", 'taliesin')
        api.destory_user(39)

    @responses.activate
    def test_user_search_no_query(self):
        responses.reset()
        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/verify'),
                      body="{\"id\": 41}",
                      status=200,
                      content_type='application/json')

        search_fixture = json.loads(load_fixture('users/search.json'))
        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/search'),
                      body=json.dumps(search_fixture),
                      status=200,
                      content_type='application/json')

        api = CsaAPI("admin", 'taliesin')
        response = api.search()

        nose.tools.assert_list_equal(search_fixture, response)

    @responses.activate
    def test_user_search_with_query(self):
        responses.reset()
        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/verify'),
                      body="{\"id\": 41}",
                      status=200,
                      content_type='application/json')

        search_fixture = json.loads(load_fixture('users/search.json'))
        search_fixture = search_fixture[:1]
        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/search'),
                      body=json.dumps(search_fixture),
                      status=200,
                      content_type='application/json')

        api = CsaAPI("admin", 'taliesin')
        response = api.search()
        nose.tools.assert_list_equal(search_fixture, response)

    @responses.activate
    @nose.tools.raises(requests.exceptions.HTTPError)
    def test_user_cannot_search(self):
        responses.reset()
        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/verify'),
                      body="{\"id\": 39}",
                      status=200,
                      content_type='application/json')

        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/search'),
                      status=422,
                      content_type='application/json')

        api = CsaAPI("cwl39", 'taliesin')
        response = api.search()


    ##########################################################################
    # Broadcast tests
    ##########################################################################

    @responses.activate
    def test_create_broadcast(self):
        responses.reset()

        fixture = load_fixture("broadcasts/1.json")
        fixture = json.loads(fixture)
        def check_broadcast_was_created(request):
            nose.tools.assert_dict_equal(fixture, json.loads(request.body))
            return (200, {}, {})

        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/verify'),
                      body="{\"id\": 41}",
                      status=200,
                      content_type='application/json')

        responses.add_callback(responses.POST,
                      CsaAPI._build_end_point_uri('/broadcasts/create'),
                      callback=check_broadcast_was_created,
                      content_type='application/json')

        api = CsaAPI("admin", 'taliesin')
        api.create_broadcast(fixture)

    @responses.activate
    def test_get_broadcast(self):
        responses.reset()

        fixture = load_fixture("broadcasts/1.json")
        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/verify'),
                      body="{\"id\": 41}",
                      status=200,
                      content_type='application/json')

        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/broadcasts/show/:id',
                                                 {':id': '1'}),
                      body=fixture,
                      status=200,
                      content_type='application/json')

        api = CsaAPI("admin", 'taliesin')
        broadcast = api.get_broadcast(1)
        nose.tools.assert_dict_equal(json.loads(fixture), broadcast)

    @responses.activate
    def test_destory_broadcast(self):
        responses.reset()

        def assert_delete(request):
            nose.tools.assert_equal(responses.DELETE, request.method)
            return (200, {}, {})

        fixture = load_fixture("broadcasts/1.json")
        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/verify'),
                      body="{\"id\": 41}",
                      status=200,
                      content_type='application/json')

        responses.add_callback(responses.DELETE,
                      CsaAPI._build_end_point_uri('/broadcasts/destroy/:id',
                                                 {':id': '1'}),
                      callback=assert_delete,
                      content_type='application/json')

        api = CsaAPI("admin", 'taliesin')
        broadcast = api.destroy_broadcast(1)

    @responses.activate
    def test_get_broadcasts(self):
        responses.reset()

        fixture = load_fixture("broadcasts.json")
        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/users/verify'),
                      body="{\"id\": 41}",
                      status=200,
                      content_type='application/json')

        responses.add(responses.GET,
                      CsaAPI._build_end_point_uri('/broadcasts'),
                      body=fixture,
                      status=200,
                      content_type='application/json')

        api = CsaAPI("admin", 'taliesin')
        broadcasts = api.get_broadcasts()
        nose.tools.assert_list_equal(json.loads(fixture), broadcasts)
