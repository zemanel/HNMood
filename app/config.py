# -*- coding: utf-8 -*-
"""App configuration."""
import os

# fill in local_settings.py
ALCHEMY_API_KEY = None

try:
    from local_settings import *
except ValueError:
    pass

config = {}
config['tipfy'] = {}
config['alchemyapi'] = {
    'API_KEY': ALCHEMY_API_KEY,
}
port = os.environ['SERVER_PORT']
if port and port != '80':
    config['tipfy']['server_name'] = '%s:%s' % (os.environ['SERVER_NAME'], port)
else:
    config['tipfy']['server_name'] = os.environ['SERVER_NAME']