# -*- coding: utf-8 -*-
import logging
from tipfy.app import Response
from tipfy.handler import RequestHandler
from tipfyext.jinja2 import Jinja2Mixin

logger = logging.getLogger(__name__)

class HomeHandler(RequestHandler, Jinja2Mixin):
    def get(self):
        context = {
        }
        key = self.app.config['alchemyapi']['API_KEY']
        return self.render_response('home.html', **context)

class PollHNSearchHandler(RequestHandler):
    '''
    Poll HNSearch API for news comments and create tasks for sentiment analysis
    '''
    pass
    
class PollAlchemySAHandler(RequestHandler):
    '''
    Poll Alchemy API sentimental analisys for a news comment
    '''
    pass