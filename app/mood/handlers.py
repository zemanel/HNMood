# -*- coding: utf-8 -*-
import logging
from django.utils import simplejson as json

from tipfy.app import Response
from tipfy.handler import RequestHandler
from tipfyext.jinja2 import Jinja2Mixin

from .models import NewsItem

logger = logging.getLogger(__name__)

class HomePage(RequestHandler, Jinja2Mixin):
    def get(self):
        return self.render_response('home.html', **{
            'baseurl' : self.url_for('home', _full=True),
            'bookmarklet_src' :    self.url_for('bookmarklet-js', _full=True),
        })

class BookmarkletPage(RequestHandler, Jinja2Mixin):
    def get(self):
        return self.render_response('bookmarklet.js', ** {
            'baseurl' : self.url_for('home', _full=True),
        })

class NewsItemDetail(RequestHandler, Jinja2Mixin):
    def get(self, itemid):
        '''Returns the json for a news item comment 
        '''
        jsoncallback = self.request.args.get('jsoncallback', None)
        itemid = str(itemid)
        newsitem = NewsItem.get_by_key_name(itemid) or self.abort(404)
        json_response = json.dumps({
            'itemid': itemid,
            'is_sentiment_processed' : newsitem.is_sentiment_processed,
            'sentiment_type': newsitem.sentiment_type,
            'sentiment_score': newsitem.sentiment_score,
            'sentiment_status': newsitem.sentiment_status,
            'sentiment_status_info': newsitem.sentiment_status_info,
            '':'',
        }, indent=2)
        if jsoncallback is None:
            return Response(json_response)
        else:
            return Response("%s(%s)" % (jsoncallback, json_response))
