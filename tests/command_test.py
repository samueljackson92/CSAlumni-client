import unittest
import nose.tools
import responses
import json
import os

from click.testing import CliRunner
from requests.exceptions import HTTPError
from test_helpers import *
from csa_client import constants
from csa_client.command import *

class TestCommand:

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
