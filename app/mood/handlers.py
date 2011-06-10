# -*- coding: utf-8 -*-
import logging
import urllib
import urllib2
from django.utils import simplejson as json
from google.appengine.ext import db

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

class PollHNSearchJob(RequestHandler):
    def get(self):
        '''Poll HNSearch API for news comments and create tasks for sentiment analysis
        '''
        #url = "http://api.thriftdb.com/api.hnsearch.com/items/_search?filter[fields][type]=comment&filter[fields][create_ts]=[NOW-30MINUTES%20TO%20NOW]&sortby=create_ts%20desc&limit=100&pretty_print=true"
        url = "http://api.thriftdb.com/api.hnsearch.com/items/_search?" + urllib.urlencode({
            'filter[fields][type]' : 'comment',
            'filter[fields][create_ts]' : '[NOW-30MINUTES TO NOW]',
            'sortby' : 'create_ts desc',
            'limit' : 100,
            'pretty_print': True
        })
        try:
            result = urllib2.urlopen(url)
            content = json.loads(result.read())
            self._parse_results(content['results'])
        except Exception, e:
            logger.exception(e)
            return Response('Application error', status=500)
        return Response('OK', status=200)

    def _parse_results(self, results):
        '''stores news items in the datastore
        '''
        for item in results:
            #logger.debug(item)
            newsitem = NewsItem.get_or_insert(key_name=str(item['item']['id']), text=item['item']['text'])
            #TODO: add task

            #logger.info(newsitem)
#            newsitem.sentiment_type = 'positive'
#            newsitem.sentiment_score = float('-0.100542')

class PollAlchemyTask(RequestHandler):
    '''
    Poll Alchemy API Sentimental Analisys for processing a news comment
    '''
    def get(self):
        api_key = self.app.config['alchemyapi']['API_KEY']
        itemid = self.request.args.get('itemid', None)
        newsitem = NewsItem.get_by_key_name(itemid)
        url = "http://access.alchemyapi.com/calls/text/TextGetTextSentiment"
        try:
            result = urllib2.urlopen(url, urllib.urlencode({
            'apikey' : api_key,
            'outputMode' : 'json',
            'text' : newsitem.text
            }))
            content = json.loads(result.read())
            logger.debug(content)
            if content['status']=='OK':
                newsitem.sentiment_type = content['docSentiment']['type']
                newsitem.sentiment_score =  float(content['docSentiment']['score'])
                newsitem.put()
            else:
                raise Exception(content['statusInfo'])
        except Exception, e:
            logger.exception(e)
            return Response('Application error', status=500)
        return Response('OK', status=200)








