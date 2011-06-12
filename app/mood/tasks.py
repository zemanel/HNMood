# -*- coding: utf-8 -*-
import logging
import datetime
from django.utils import simplejson as json
from tipfy.app import Response
from tipfy.handler import RequestHandler

from .models import NewsItem
from .alchemyapi import AlchemyAPI
from .hnsearchapi import HNSearchAPI

logger = logging.getLogger(__name__)

class PollHNSearchTask(RequestHandler):
  '''Poll HNSearch API
  '''
  def get(self):
    try:
      created_from = self.request.args.get('created_from', None)
      created_to = self.request.args.get('created_to', None)
      start = self.request.args.get('start', None)
      limit = self.request.args.get('limit', None)
      api = HNSearchAPI()
      result = api.search(created_from=created_from, created_to=created_to, start=start, limit=limit)
      content = json.loads(result, encoding="utf-8")
      logger.info('Got %s hits' % content['hits'])
      self._parse_results(content['results'])
    except Exception, e:
      logger.exception(e)
      return Response('Application error', status=500)
    return Response('OK', status=200)
    
  def _parse_results(self, results):
    '''stores news items in the datastore
    '''
    for item in results:
      keyname = str(item['item']['id'])
      newsitem = NewsItem.get_by_key_name(keyname)
      if newsitem is not None:
        props = {
          'text' : item['item']['text'],
          'username' : item['item']['username'],
          'type': item['item']['type'],
          'create_ts' : datetime.datetime.strptime(item['item']['create_ts'], '%Y-%m-%dT%H:%M:%SZ'),
          'parent_id' : int(item['item']['parent_id'])
        }
        newsitem = NewsItem(key_name=keyname, **props)
        logger.debug("Created NewsItem %s" % keyname)
      logger.debug("NewsItem %s already exists" % keyname)

class PollAlchemyTask(RequestHandler):
  '''Poll Alchemy API Sentimental Analisys for processing a news comment item
  '''
  def get(self):
    apikey = self.app.config['mood.alchemyapi']['API_KEY']
    itemid = self.request.args.get('itemid', None)
    newsitem = NewsItem.get_by_key_name(itemid)
    if newsitem is not None:
      try:
        api = AlchemyAPI(apikey=apikey)
        result = api.request(unicode(newsitem.text).encode('utf-8'))
        content = json.loads(result.read())
        #logger.debug(content)
        if content['status'] == 'OK':
          newsitem.sentiment_type = content['docSentiment']['type']
          if content['docSentiment']['type'] != 'neutral':
            newsitem.sentiment_score = float(content['docSentiment']['score'])
          else:
            newsitem.sentiment_score = .0
          newsitem.is_sentiment_processed = True
          newsitem.put()
          logger.info("Analyzed item %s" % itemid)
        else:
          raise Exception(content['statusInfo'])
      except Exception, e:
        logger.exception(e)
        return Response('Application error', status=500)
      return Response('OK', status=200)
    return Response('Item %s not found' % itemid, status=404)