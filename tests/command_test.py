import unittest
import nose.tools
import responses
import json
import os

from click.testing import CliRunner
from requests.exceptions import HTTPError
from test_helpers import *
from csa_client import constants
from csa_client import RequestHandler
from csa_client.command import *

class CommandTests(unittest.TestCase):

    def tearDown(self):
        responses.reset()
        if os.path.isfile(constants.TOKEN_FILE):
            os.remove(constants.TOKEN_FILE)

    @responses.activate
    def test_authenticate(self):
        runner = CliRunner()
        mock_auth_response()

        with runner.isolated_filesystem():
            result = runner.invoke(authorize, input='admin\ntaliesin\ntaliesin')
            nose.tools.assert_false(result.exception)
            nose.tools.assert_equal(0, result.exit_code)

    ##########################################################################
    # User tests
    ##########################################################################

    @responses.activate
    def test_create_user(self):
        runner = CliRunner()
        mock_auth_response()

        url = RequestHandler._build_end_point_uri('/users/create')
        responses.add(responses.POST, url, status=200)

        with runner.isolated_filesystem():
            result = runner.invoke(authorize, input='admin\ntaliesin\ntaliesin')
            nose.tools.assert_false(result.exception)
            nose.tools.assert_equal(0, result.exit_code)

            user_params = ['sam', 'jackson', 'slj11@aber.ac.uk', '1985', 'n', 'slj11', 'password', 'password']
            user_params = '\n'.join(user_params)

            result = runner.invoke(cli, ['users', 'create'], input=user_params)
            nose.tools.assert_false(result.exception)
            nose.tools.assert_equal(0, result.exit_code)

    @responses.activate
    def test_update_user(self):
        runner = CliRunner()
        mock_auth_response()
        mock_show_user_response(41)

        url = RequestHandler._build_end_point_uri('/users/update/:id', {':id': '41'})
        responses.add(responses.PUT, url, status=200)

        with runner.isolated_filesystem():
            result = runner.invoke(authorize, input='admin\ntaliesin\ntaliesin')
            nose.tools.assert_false(result.exception)
            nose.tools.assert_equal(0, result.exit_code)

            result = runner.invoke(cli, ['users', 'update', '41', '--firstname=samuel'])
            nose.tools.assert_false(result.exception)
            nose.tools.assert_equal(0, result.exit_code)


    @responses.activate
    def test_show_user(self):
        runner = CliRunner()
        mock_auth_response()
        mock_show_user_response(41)

        with runner.isolated_filesystem():
            result = runner.invoke(authorize, input='admin\ntaliesin\ntaliesin')
            nose.tools.assert_false(result.exception)
            nose.tools.assert_equal(0, result.exit_code)

            result = runner.invoke(cli, ['users', 'show', '41'])
            nose.tools.assert_false(result.exception)
            nose.tools.assert_equal(0, result.exit_code)

    @responses.activate
    def test_search_users(self):
        runner = CliRunner()
        mock_auth_response()

        fixture = load_fixture('users/search.json')
        url = RequestHandler._build_end_point_uri('/users/search')
        responses.add(responses.GET, url, status=200, body=fixture)

        with runner.isolated_filesystem():
            result = runner.invoke(authorize, input='admin\ntaliesin\ntaliesin')
            nose.tools.assert_false(result.exception)
            nose.tools.assert_equal(0, result.exit_code)

            result = runner.invoke(cli, ['users', 'search', '"Loftus"'])
            nose.tools.assert_false(result.exception)
            nose.tools.assert_equal(0, result.exit_code)

    @responses.activate
    def test_destroy_user(self):
        runner = CliRunner()
        mock_auth_response()

        url = RequestHandler._build_end_point_uri('/users/destroy/:id', {':id': '41'})
        responses.add(responses.DELETE, url, status=200)

        with runner.isolated_filesystem():
            result = runner.invoke(authorize, input='admin\ntaliesin\ntaliesin')
            nose.tools.assert_false(result.exception)
            nose.tools.assert_equal(0, result.exit_code)

            result = runner.invoke(cli, ['users', 'destroy', '41'])
            nose.tools.assert_false(result.exception)
            nose.tools.assert_equal(0, result.exit_code)

    ##########################################################################
    # Broadcast tests
    ##########################################################################

    @responses.activate
    def test_create_broadcast(self):
        runner = CliRunner()
        mock_auth_response()
        mock_show_user_response(41)

        url = RequestHandler._build_end_point_uri('/broadcasts/create')
        responses.add(responses.POST, url, status=200)

        with runner.isolated_filesystem():
            result = runner.invoke(authorize, input='admin\ntaliesin\ntaliesin')
            nose.tools.assert_false(result.exception)
            nose.tools.assert_equal(0, result.exit_code)

            result = runner.invoke(cli, ['broadcasts', 'create', '"message"', '-f twitter'])
            nose.tools.assert_false(result.exception)
            nose.tools.assert_equal(0, result.exit_code)

    @responses.activate
    def test_search_broadcasts(self):
        runner = CliRunner()
        mock_auth_response()

        fixture = load_fixture('broadcasts/search.json')
        url = RequestHandler._build_end_point_uri('/broadcasts/search')
        responses.add(responses.GET, url, status=200, body=fixture)

        with runner.isolated_filesystem():
            result = runner.invoke(authorize, input='admin\ntaliesin\ntaliesin')
            nose.tools.assert_false(result.exception)
            nose.tools.assert_equal(0, result.exit_code)

            result = runner.invoke(cli, ['broadcasts', 'search', '"Chris"'])
            nose.tools.assert_false(result.exception)
            nose.tools.assert_equal(0, result.exit_code)

    @responses.activate
    def test_show_broadcast(self):
        runner = CliRunner()
        mock_auth_response()

        fixture = load_fixture('broadcasts/1.json')
        url = RequestHandler._build_end_point_uri('/broadcasts/show/:id', {':id': '1'})
        responses.add(responses.GET, url, status=200, body=fixture)

        with runner.isolated_filesystem():
            result = runner.invoke(authorize, input='admin\ntaliesin\ntaliesin')
            nose.tools.assert_false(result.exception)
            nose.tools.assert_equal(0, result.exit_code)

            result = runner.invoke(cli, ['broadcasts', 'show', '1'])
            nose.tools.assert_false(result.exception)
            nose.tools.assert_equal(0, result.exit_code)

    @responses.activate
    def test_destroy_broadcast(self):
        runner = CliRunner()
        mock_auth_response()

        url = RequestHandler._build_end_point_uri('/broadcasts/destroy/:id', {':id': '1'})
        responses.add(responses.DELETE, url, status=200)

        with runner.isolated_filesystem():
            result = runner.invoke(authorize, input='admin\ntaliesin\ntaliesin')
            nose.tools.assert_false(result.exception)
            nose.tools.assert_equal(0, result.exit_code)

            result = runner.invoke(cli, ['broadcasts', 'destroy', '1'])
            nose.tools.assert_false(result.exception)
            nose.tools.assert_equal(0, result.exit_code)
