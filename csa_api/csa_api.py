__author__ = "Samuel Jackson"
__date__ = "November 26, 2014"
__license__ = "MIT"

import requests
import re

from constants import *

class CsaAPI(object):
    """ Access the REST resources on the CSA application.

    :param username: CSA application username
    :param password: CSA application password
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def make_request(self, end_point, end_point_vars={}):
        """Make a request to Csa API at the specified end point

        :param end_point: string representing the end resource request
        :param end_point_vars: dictionary of variables to be replaced in the uri
        """
        url = self._build_end_point_uri(end_point, end_point_vars)

        session = requests.Session()
        req = requests.Request(END_POINTS[end_point], url,
                               auth=(self.username, self.password))
        prepped = req.prepare()
        response = session.send(prepped)

        #check the response was ok
        response.raise_for_status()

        return response.json()

    def _build_end_point_uri(self, end_point, params={}):
        """Build a url to a API end point.

        This takes a optional dictionary of regex parameters to replace in the
        end point url. I.e. replacing :id in users/show/:id

        :param end_point: The end point to build the uri for
        :param params: A dictionary parameters to replace in the uri
        """
        if end_point not in END_POINTS:
            raise KeyError("Unsupported application endpoint.")

        uri = end_point + '.' + CONTENT_TYPE
        for key, value in params.iteritems():
            if key in uri:
                uri = re.sub(key, str(value), uri)

        if ":" in uri:
            raise ValueError("Some parameters were not replaced in uri.\
                             Cannot build valid application url.")

        return self._build_domain_address() + uri

    def _build_domain_address(self):
        """ Build the base url of the api end points """
        return PROTOCOL + ":".join((DOMAIN, PORT))
