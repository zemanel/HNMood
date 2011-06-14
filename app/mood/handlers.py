# -*- coding: utf-8 -*-
import logging
from django.utils import simplejson as json

from tipfy.app import Response
from tipfy.handler import RequestHandler
from tipfyext.jinja2 import Jinja2Mixin
from google.appengine.api import memcache

from .models import NewsItem

logger = logging.getLogger(__name__)

class HomePage(RequestHandler, Jinja2Mixin):
    def get(self):
        CACHE_ENABLED = self.app.config['mood']['CACHE_ENABLED']
        memcachekey = "handler_home"
        response = memcache.get(memcachekey)
        if response is None:
            response = self.render_response('home.html', **{
                'baseurl' : self.url_for('home', _full=True),
                'bookmarklet_src' : self.url_for('bookmarklet-js', _full=True),
            })
            if CACHE_ENABLED:
                memcache.set(memcachekey, response, 60*60)
        return response

class BookmarkletPage(RequestHandler, Jinja2Mixin):
    def get(self):
        CACHE_ENABLED = self.app.config['mood']['CACHE_ENABLED']
        memcachekey = "handler_bookmarklet"
        response = memcache.get(memcachekey)
        if response is None:
            response = self.render_response('bookmarklet.js', ** {
                'baseurl' : self.url_for('home', _full=True),
            })
            if CACHE_ENABLED:
                memcache.set(memcachekey, response, 60*60)
        return response

class NewsItemDetail(RequestHandler, Jinja2Mixin):
    def get(self, itemid):
        '''Returns the json for a news item comment 
        '''
        CACHE_ENABLED = self.app.config['mood']['CACHE_ENABLED']
        jsoncallback = self.request.args.get('jsoncallback', None)
        itemid = str(itemid)
        memcachekey = "handler_newsitem_detail_%s" % itemid 
        response = memcache.get(memcachekey)
        if response is None:
            newsitem = NewsItem.get_by_key_name(itemid)
            if newsitem is not None:
                response = json.dumps({
                    'itemid': itemid,
                    'is_sentiment_processed' : newsitem.is_sentiment_processed,
                    'sentiment_type': newsitem.sentiment_type,
                    'sentiment_score': newsitem.sentiment_score,
                    'sentiment_status': newsitem.sentiment_status,
                    'sentiment_status_info': newsitem.sentiment_status_info,
                }, indent=2)
            else:
                response = json.dumps({
                    'itemid': itemid,
                    'is_sentiment_processed' : False,
                }, indent=2)
            if jsoncallback is not None:
                response = "%s(%s)" % (jsoncallback, response)
            if CACHE_ENABLED:
                memcache.set(memcachekey, response, 5*60)
        return response
