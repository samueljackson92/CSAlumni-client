__author__ = "Samuel Jackson"
__date__ = "November 26, 2014"
__license__ = "MIT"

# protocal used by the api
PROTOCOL = 'https://'
# domain of the endpoints
DOMAIN = 'localhost'
# port of the endpoints
PORT = '3001'
# Content type that the application communicates in
CONTENT_TYPE = 'json'
# Whether to verify the ssl certificate of the website
VERIFY_SSL = False

TOKEN_FILE = '.tokens.json'

END_POINTS = {
    "/oauth/token": "POST",

    "/users/verify": "GET",
    "/users/search": "GET",
    "/users/create": "POST",
    "/users/show/:id": "GET",
    "/users/update/:id": "PUT",
    "/users/destory/:id": "DELETE",

    "/broadcasts": "GET",
    "/broadcasts/create": "POST",
    "/broadcasts/show/:id": "GET",
    "/broadcasts/destroy/:id": "DELETE",

    "/coffee": "BREW"
}
