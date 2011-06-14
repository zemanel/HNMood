# -*- coding: utf-8 -*-
"""App configuration."""
import os
DEVEL = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

# fill in local_settings.py
ALCHEMY_API_KEY = None

try:
    from local_settings import *
except ValueError:
    pass

config = {
    'tipfy' : {}
}

config['mood'] = {
    'CACHE_ENABLED': not DEVEL,
    'ALCHEMYAPI_KEY': ALCHEMY_API_KEY,
}