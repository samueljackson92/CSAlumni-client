import unittest
import nose.tools
import pickledb
import os

from test_helpers import *
from csa_client.token_cache import TokenCache

class TokenCacheTest(unittest.TestCase):

    def setUp(self):
        self.tokens = {'access_token': 'abcd', 'refresh_token': 'abcd'}

    def tearDown(self):
        if os.path.isfile(constants.TOKEN_FILE):
            os.remove(constants.TOKEN_FILE)

    def test_cache_and_load(self):
        TokenCache.cache_tokens(self.tokens)
        nose.tools.assert_true(os.path.isfile(constants.TOKEN_FILE))

        tokens = TokenCache.load_tokens()
        nose.tools.assert_dict_equal(self.tokens, tokens)
