__author__ = "Samuel Jackson"
__date__ = "December 2, 2014"
__license__ = "MIT"

import requests
import json

from constants import *
from request_handler import RequestHandler

class OAuth2ResourceOwner(RequestHandler):
    """ Handles retrieving resources from the specified end-points.

    This extension adds functionality for the resource owner OAuth2
    specification. Authentication is originally supplied by the user via their
    username and password (resource credentials). Access and refresh tokens are
    obtained and can be cached locally. This class will automatically handle
    refreshing the tokens ase required. See RFC6749 for more info.

    :param token_endpoint: the end point to request oauth2 tokens from.
    """
    def __init__(self, token_endpoint):
        super(OAuth2ResourceOwner, self).__init__()
        self.token_endpoint = token_endpoint

    def request_auth_with_client_credentials(self, username, password):
        """Request authentication using the resource owners credentials

        This accquires the access tokens for the first time and discards the
        username and password once used.

        :param username: username of the resource owner
        :param password: password of the resource owner
        """
        payload = {'grant_type': 'password', 'username': username, 'password': password}

        response = self.make_request(self.token_endpoint, params=payload)
        json_response = response.json()

        print json_response

        if 'access_token' not in json_response:
            raise ValueError("Access token not present in response!")

        if 'refresh_token' not in json_response:
            raise ValueError("Refresh token not present in response!")

        self._refresh_auth_state(json_response)

    def request_auth_with_refresh_token(self):
        """Use a refresh token to generate a new oauth access token."""
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }

        response = self.make_request(self.token_endpoint, params=payload)
        json_response = response.json()
        self._refresh_auth_state(json_response)

    def make_request(self, end_point, end_point_vars={}, params={}):
        """Make a request to Csa API at the specified end point

        This method is override from the request handler class and will refresh
        the oauth tokens if neccessary.

        :param end_point: string representing the end resource request
        :param end_point_vars: dictionary of variables to be replaced in the uri
        :param params: dictionary of parameters to be passed via GET/POST
        """
        response = super(OAuth2ResourceOwner, self) \
                        .make_request(end_point, end_point_vars, params)


        if response.status_code == requests.codes.unauthorized:
            if not 'error' in response.text:
                self.request_auth_with_refresh_token()
                response = super(OAuth2ResourceOwner, self) \
                                .make_request(end_point, end_point_vars, params)

        response.raise_for_status()
        return response

    def get_tokens(self):
        """Get dictionary of tokens"""
        if self.access_token and self.refresh_token:
            token_data = {
              'access_token': self.access_token,
              'refresh_token': self.refresh_token
            }
            return token_data

    def set_tokens(self,token_data):
        """Get dictionary of tokens"""
        self._refresh_auth_state(token_data)

    def _refresh_auth_state(self, tokens):
        """Refresh the access tokens used to authenticate requests

        :param tokens: dict containing the access_tokens
        """
        self.access_token = tokens['access_token']
        self.refresh_token = tokens['refresh_token']
        self.session.auth = OAuth2Tokens(self.access_token)


class OAuth2Tokens(requests.auth.AuthBase):
    """Authorization extensions of the requests.auth.AuthBase class

    Adds support for appending the access token to a request.

    :param token: access token used with the resource request
    """
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        #append the access token to the body
        body = json.loads(r.body)
        body.update({'access_token': self.token})
        r.body = json.dumps(body)
        return r
