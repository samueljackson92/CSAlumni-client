__author__ = "Samuel Jackson"
__date__ = "November 26, 2014"
__license__ = "MIT"

# protocal used by the api
PROTOCOL = 'http://'
# domain of the endpoints
DOMAIN = 'localhost'
# port of the endpoints
PORT = '3000'
# Content type that the application communicates in
CONTENT_TYPE = 'json'

END_POINTS = {
    "/users/verify": "GET",
    "/users/search": "GET",
    "/users/show/:id": "GET",
    "/users/update/:id": "PUT",
    "/users/destory/:id": "DELETE",
}
