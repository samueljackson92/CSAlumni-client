__author__ = "Samuel Jackson"
__date__ = "December 2, 2014"
__license__ = "MIT"

import os
import pickledb

from constants import *

class TokenCache(object):
    @staticmethod
    def cache_tokens(token_data):
        """Save oauth tokens to a local file between commands"""
        if not token_data:
            raise ValueError("Token data does not exist.")

        db = pickledb.load(TOKEN_FILE, False)
        db.set('access_token', token_data['access_token'])
        db.set('refresh_token', token_data['refresh_token'])
        db.dump()

    @staticmethod
    def load_tokens():
        """Load oauth tokens cached in a local file"""
        if not os.path.isfile(TOKEN_FILE):
            raise ValueError("Token cache file does not exist.")

        db = pickledb.load(TOKEN_FILE, False)
        tokens = {}
        tokens['access_token'] = db.get('access_token')
        tokens['refresh_token'] = db.get('refresh_token')
        return tokens
