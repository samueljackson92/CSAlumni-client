__author__ = "Samuel Jackson"
__date__ = "December 2, 2014"
__license__ = "MIT"

import json
import requests
import re

from constants import *

class RequestHandler(object):
    """ Handles retrieving resources from the specified end-points."""
    def __init__(self):
        headers={
            "content-type": "application/json",
            "x-api-client-type": "application/json"
        }

        self.session = requests.Session()
        self.session.headers.update(headers)

    def make_request(self, end_point, end_point_vars={}, params={}):
        """Make a request to Csa API at the specified end point

        :param end_point: string representing the end resource request
        :param end_point_vars: dictionary of variables to be replaced in the uri
        :param params: dictionary of parameters to be passed via GET/POST
        """
        url = RequestHandler._build_end_point_uri(end_point, end_point_vars)

        req = requests.Request(END_POINTS[end_point],
                               url,
                               data=json.dumps(params))

        prepped = self.session.prepare_request(req)
        response = self.session.send(prepped, verify=VERIFY_SSL)
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

        return RequestHandler._build_domain_address() + uri

    @staticmethod
    def _build_domain_address():
        """ Build the base url of the api end points """
        return PROTOCOL + ":".join((DOMAIN, PORT))
