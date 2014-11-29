__title__ = 'CsaAPI'
__version__ = '0.1.0'
__author__ = 'Samuel Jackson'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014 Samuel Jackson'

try:
    from .csa_api import CsaAPI
    from .json_object import JSONObject
except:
    pass

__all__ = [
    'CsaAPI',
    'JSONObject'
]
