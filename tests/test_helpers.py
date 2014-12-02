__author__ = "Samuel Jackson"
__date__ = "November 26, 2014"
__license__ = "MIT"

import os
import json
import responses

from csa_client.request_handler import RequestHandler
from csa_client.api import CsaAPI
from csa_client import constants

FIXTURES_FOLDER = "fixtures"

def load_fixture(file_name):
    """Load a text file from the fixtures folder """
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, FIXTURES_FOLDER)
    file_name = os.path.join(path, file_name)
    with open(file_name, 'r') as file_handle:
        fixture_text = file_handle.read()
    return fixture_text

def mock_auth_response(status=200, body=None):
    if body is None:
        body = json.dumps({"access_token": "abcdef", "refresh_token": "abcdef"})

    responses.add(responses.POST,
                  RequestHandler._build_end_point_uri('/oauth/token'),
                  body=body,
                  status=status,
                  content_type='application/json')

def mock_show_user_response(user_id, status=200, body=None):

    if body is None:
        fixture = load_fixture('users/show/%d.json' % user_id)
    else:
        fixture = body

    responses.add(responses.GET,
                  RequestHandler._build_end_point_uri('/users/show/:id',
                                                {':id': user_id}),
                  body=fixture,
                  status=status,
                  content_type='application/json')

    return json.loads(fixture)
