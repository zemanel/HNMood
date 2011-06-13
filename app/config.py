# -*- coding: utf-8 -*-
"""App configuration."""
import os

# fill in local_settings.py
ALCHEMY_API_KEY = None

try:
    from local_settings import *
except ValueError:
    pass

config = {
    'tipfy' : {}
}

config['mood.alchemyapi'] = {
    'API_KEY': ALCHEMY_API_KEY,
}