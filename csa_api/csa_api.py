__author__ = "Samuel Jackson"
__date__ = "November 26, 2014"
__license__ = "MIT"

import json
import requests
import re

from json_object import JSONObject
from constants import *

class CsaAPI(object):
    """ Access the REST resources on the CSA application.

    :param username: CSA application username
    :param password: CSA application password
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)
        self.session.headers.update({"content-type": "application/json", "x-api-client-type": "application/json"})
        self.verify()

    ###########################################################################
    # User request helpers
    ###########################################################################

    def get_user(self, user_id=None):
        """Get a user record as an object

        :param user_id: the id of the user to get.
        """
        user_id = self.user_id if user_id is None else user_id
        response = self.make_request('/users/show/:id', {":id": user_id})
        user = response.json()
        user["id"] = user_id
        return user

    def update_user(self, user):
        """Update a user record

        :param user: The user to update.
        """
        self.make_request('/users/update/:id',
                          end_point_vars={":id": user["id"]},
                          params=user)

    def destory_user(self, user_id=None):
        """Destory a user record

        :param user_id: the ide of the user to delete
        """
        user_id = self.user_id if user_id is None else user_id
        self.make_request('/users/destory/:id', {":id": user_id})


    def search(self, query=''):
        response = self.make_request('/users/search', params={'q': query})
        json_reponse = response.json()
        return json_reponse

    ###########################################################################
    # Broadcast request helpers
    ###########################################################################

    def get_broadcast(self, broadcast_id):
        """Get a broadcast record

        :param broadcast_id: the id of the broadcast to get.
        """
        response = self.make_request('/broadcasts/show/:id',
                                    {":id": broadcast_id})
        json_reponse = response.json()
        return json_reponse

    def get_broadcasts(self):
        """Get all broadcasts on the server."""
        response = self.make_request('/broadcasts')
        json_reponse = response.json()
        return json_reponse

    def destroy_broadcast(self, broadcast_id):
        """Destory a broadcast record

        :param broadcast_id: the id of the broadcast to destory.
        """
        self.make_request('/broadcasts/destroy/:id', {":id": broadcast_id})

    def verify(self):
        """Verify a user can log in and get their user id"""
        response = self.make_request('/users/verify')
        json_reponse = response.json()
        self.user_id = json_reponse["id"]

    def make_request(self, end_point, end_point_vars={}, params={}):
        """Make a request to Csa API at the specified end point

        :param end_point: string representing the end resource request
        :param end_point_vars: dictionary of variables to be replaced in the uri
        :param params: dictionary of parameters to be passed via GET/POST
        """
        url = CsaAPI._build_end_point_uri(end_point, end_point_vars)
        req = requests.Request(END_POINTS[end_point], url, data=json.dumps(params))
        prepped = self.session.prepare_request(req)
        response = self.session.send(prepped)
        #check the response was ok
        response.raise_for_status()
        return response

    @staticmethod
    def _build_end_point_uri(end_point, params={}):
        """Build a url to a API end point.

        This takes a optional dictionary of regex parameters to replace in the
        end point url. I.e. replacing :id in users/show/:id

        :param end_point: The end point to build the uri for
        :param params: A dictionary parameters to replace in the uri
        """
        if end_point not in END_POINTS:
            raise KeyError("Unsupported application endpoint: %s" % end_point)

        uri = end_point + '.' + CONTENT_TYPE
        for key, value in params.iteritems():
            if key in uri:
                uri = re.sub(key, str(value), uri)

        if ":" in uri:
            raise ValueError("Some parameters were not replaced in uri.\
                             Cannot build valid application url.")

        return CsaAPI._build_domain_address() + uri

    @staticmethod
    def _build_domain_address():
        """ Build the base url of the api end points """
        return PROTOCOL + ":".join((DOMAIN, PORT))
