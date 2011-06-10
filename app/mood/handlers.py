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

class HomePage(RequestHandler, Jinja2Mixin):
    def get(self):
        context = {
        }
        return self.render_response('home.html', **context)

class NewsItemDetail(RequestHandler, Jinja2Mixin):
    def get(self, itemid):
        '''Returns the json for a news item comment 
        '''
        #itemid = self.request.args.get('itemid', None)
        itemid = str(itemid)
        newsitem = NewsItem.get_by_key_name(itemid) or self.abort(404)
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
        api_key = self.app.config['alchemyapi']['API_KEY']
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








