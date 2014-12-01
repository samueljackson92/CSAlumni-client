__author__ = "Samuel Jackson"
__date__ = "November 26, 2014"
__license__ = "MIT"

import os

from csa_client import CsaAPI

FIXTURES_FOLDER = "fixtures"

def load_fixture(file_name):
    """Load a text file from the fixtures folder """
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, FIXTURES_FOLDER)
    file_name = os.path.join(path, file_name)
    with open(file_name, 'r') as file_handle:
        fixture_text = file_handle.read()
    return fixture_text


def mock_verify_response(responses, user_id):
    responses.add(responses.GET,
                  CsaAPI._build_end_point_uri('/users/verify'),
                  body="{\"id\": \"%s\"}" % str(user_id),
                  status=200,
                  content_type='application/json')

def mock_show_user_response(responses, user_id, fixture):
    responses.add(responses.GET,
                  CsaAPI._build_end_point_uri('/users/show/:id',
                                                {':id': user_id}),
                  body=fixture,
                  status=200,
                  content_type='application/json')

def mock_update_user_response(responses, user_id):
    responses.add(responses.PUT,
                  CsaAPI._build_end_point_uri('/users/update/:id',
                                                {':id': user_id}),
                  status=200,
                  content_type='application/json')
