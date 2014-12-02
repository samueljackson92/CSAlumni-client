__author__ = "Samuel Jackson"
__date__ = "December 2, 2014"
__license__ = "MIT"

import os
import json

from constants import *

class TokenCache(object):
    @staticmethod
    def cache_tokens(token_data):
        """Save oauth tokens to a local file between commands"""
        with open(TOKEN_FILE, 'w') as token_file:
            json.dump(token_data, token_file)

    @staticmethod
    def load_tokens():
        """Load oauth tokens cached in a local file"""
        if not os.path.isfile(TOKEN_FILE):
            raise ValueError("Token cache file does not exist.")

        with open(TOKEN_FILE, 'r') as token_file:
            token_data = json.load(token_file)
            return token_data
