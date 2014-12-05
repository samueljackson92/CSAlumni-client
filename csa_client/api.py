__author__ = "Samuel Jackson"
__date__ = "November 26, 2014"
__license__ = "MIT"

from oauth import OAuth2ResourceOwner
from token_cache import TokenCache
from constants import *

class CsaAPI(object):
    """ Access the REST resources on the CSA application.

    :param username: CSA application username
    :param password: CSA application password
    """
    def __init__(self, tokens=None, username=None, password=None):
        self.session = OAuth2ResourceOwner('/oauth/token')

        if username is None and password is None:
            self.session.set_tokens(tokens)
        else:
            self.session.request_auth_with_client_credentials(username, password)

        self.verify()

    ###########################################################################
    # User request helpers
    ###########################################################################

    def create_user(self, user):
        """Create a new user

        :param user: the user object to create
        """
        self.session.make_request('/users/create', params=user)

    def get_user(self, user_id=None):
        """Get a user record as an object

        :param user_id: the id of the user to get.
        """
        user_id = self.user_id if user_id is None else user_id
        response = self.session.make_request('/users/show/:id', {":id": user_id})
        user = response.json()
        user["id"] = user_id
        return user

    def update_user(self, user):
        """Update a user record

        :param user: The user to update.
        """
        self.session.make_request('/users/update/:id',
                          end_point_vars={":id": user["id"]},
                          params=user)

    def destroy_user(self, user_id=None):
        """Destory a user record

        :param user_id: the ide of the user to delete
        """
        user_id = self.user_id if user_id is None else user_id
        self.session.make_request('/users/destory/:id', {":id": user_id})


    def search(self, query=''):
        response = self.session.make_request('/users/search', params={'q': query})
        json_reponse = response.json()
        return json_reponse

    ###########################################################################
    # Broadcast request helpers
    ###########################################################################

    def create_broadcast(self, broadcast):
        """Create a new broadcast

        :param broadcast: the broadcast object to create
        """
        self.session.make_request('/broadcasts/create', params=broadcast)

    def get_broadcast(self, broadcast_id):
        """Get a broadcast record

        :param broadcast_id: the id of the broadcast to get.
        """
        response = self.session.make_request('/broadcasts/show/:id',
                                    {":id": broadcast_id})
        json_reponse = response.json()
        return json_reponse

    def get_broadcasts(self):
        """Get all broadcasts on the server."""
        response = self.session.make_request('/broadcasts')
        json_reponse = response.json()
        return json_reponse

    def destroy_broadcast(self, broadcast_id):
        """Destory a broadcast record

        :param broadcast_id: the id of the broadcast to destory.
        """
        self.session.make_request('/broadcasts/destroy/:id', {":id": broadcast_id})

    ###########################################################################
    # Misc
    ###########################################################################

    def make_coffee(self):
        """ Request via BREW """
        return self.session.make_request('/coffee')

    def verify(self):
        """Get the users id from the server """
        response = self.session.make_request('/users/verify')
        json_reponse = response.json()
        self.user_id = json_reponse['id']

    def get_session(self):
        return self.session
