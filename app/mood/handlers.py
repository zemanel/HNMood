# -*- coding: utf-8 -*-
import logging
import urllib
import urllib2
import codecs
from django.utils import simplejson as json

from google.appengine.ext import db
from google.appengine.api import taskqueue

from tipfy.app import Response
from tipfy.handler import RequestHandler
from tipfyext.jinja2 import Jinja2Mixin

from models import NewsItem

logger = logging.getLogger(__name__)

MOOD_ICONS = {
    'sentiment_positive': {
        'description': 'Positive sentiment',
        'src': 'static/img/silk_icons/emoticon_happy.png',
        'width' : 16,
        'height' : 16,
        'alt': 'Positive',
    },
    'sentiment_negative': {
        'description': 'Negative sentiment',
        'src': 'static/img/silk_icons/emoticon_unhappy.png',
        'width' : 16,
        'height' : 16,
        'alt': 'Negative',
    },
    'sentiment_neutral': {
        'description': 'Neutral sentiment',
        'src': 'static/img/silk_icons/emoticon_waii.png',
        'width' : 16,
        'height' : 16,
        'alt': 'Neutral',
    },
    'sentiment_unavailable': {
        'description': 'Sentiment analisys unavailable',
        'src': 'static/img/silk_icons/help.png',
        'width' : 16,
        'height' : 16,
        'alt': 'Unavailable',
    },    
}

#for k, v in last.iteritems()

class HomePage(RequestHandler, Jinja2Mixin):
    def get(self): 
        return self.render_response('home.html', **{
            'baseurl' : self.url_for('home', _full=True),
            'bookmarklet_src' :  self.url_for('bookmarklet-js', _full=True),
            'icons' : MOOD_ICONS
        })

class BookmarkletPage(RequestHandler, Jinja2Mixin):
    def get(self):
        return self.render_response('bookmarklet.js',** {
            'baseurl' : self.url_for('home', _full=True),
            'icons' : json.dumps(self.app.config['mood.icons'])
        })

class NewsItemDetail(RequestHandler, Jinja2Mixin):
    def get(self, itemid):
        '''Returns the json for a news item comment 
        '''
        #itemid = self.request.args.get('itemid', None)
        itemid = str(itemid)
        newsitem = NewsItem.get_by_key_name(itemid) or self.abort(404)
        #logger.debug(self.app.config)
        #logger.debug(self.url_for('home', _full=True))
        return Response(json.dumps({
            'itemid': itemid,
            'is_sentiment_processed' : newsitem.is_sentiment_processed,
            'sentiment_type': newsitem.sentiment_type,
            'sentiment_score': newsitem.sentiment_score,
            '':'',
        }, indent=2))

class PollHNSearchJob(RequestHandler):
    def get(self):
        '''Poll HNSearch API for news comments and create tasks for sentiment analysis
        '''
        url = "http://api.thriftdb.com/api.hnsearch.com/items/_search?" + urllib.urlencode({
            'filter[fields][type]' : 'comment',
            'filter[fields][create_ts]' : '[NOW-30MINUTES TO NOW]',
            'sortby' : 'create_ts desc',
            'limit' : 100,
            'pretty_print': True
        })
        try:
            result = urllib2.urlopen(url)
            content = json.loads(result.read(), encoding="utf-8")
            self._parse_results(content['results'])
        except Exception, e:
            logger.exception(e)
            return Response('Application error', status=500)
        return Response('OK', status=200)

    def _parse_results(self, results):
        '''stores news items in the datastore
        '''
        for item in results:
            key = str(item['item']['id'])
            NewsItem.get_or_insert(key_name=key, text=item['item']['text'])
            logger.info("Stored item %s" % key)

class QueueAlchemyTasksJob(RequestHandler):
    def get(self):
        '''
        '''
        queue = taskqueue.Queue()
        items = NewsItem.all(keys_only=True).filter("is_sentiment_processed", False).order('-created_on').fetch(limit=100)
        for key in items:
            keyname = key.name()
            taskname = "sentimental-analisys-%s"%keyname
            task = taskqueue.Task(params={'itemid':keyname}, name=taskname, method="GET", url="/tasks/poll_alchemyapi")
            queue.add(task)
            logger.info("Created task %s" % taskname)
        return Response('OK', status=200)

class PollAlchemyTask(RequestHandler):
    '''Poll Alchemy API Sentimental Analisys for processing a news comment item
    '''
    def get(self):
        api_key = self.app.config['mood.alchemyapi']['API_KEY']
        itemid = self.request.args.get('itemid', None)
        newsitem = NewsItem.get_by_key_name(itemid)
        if newsitem is not None:
            url = "http://access.alchemyapi.com/calls/text/TextGetTextSentiment"
            try:
                result = urllib2.urlopen(url, urllib.urlencode({
                'apikey' : api_key,
                'outputMode' : 'json',
                'text' :  unicode(newsitem.text).encode('utf-8')
                }))
                content = json.loads(result.read())
                #logger.debug(content)
                if content['status']=='OK':
                    newsitem.sentiment_type = content['docSentiment']['type']
                    if content['docSentiment']['type'] != 'neutral':
                        newsitem.sentiment_score = float(content['docSentiment']['score'])
                    else:
                        newsitem.sentiment_score = .0
                    newsitem.is_sentiment_processed = True
                    newsitem.put()
                    logger.info("Analyzed item %s" %itemid)
                else:
                    raise Exception(content['statusInfo'])
            except Exception, e:
                logger.exception(e)
                return Response('Application error', status=500)
            return Response('OK', status=200)
        return Response('Item %s not found'%itemid, status=404)








