# -*- coding: utf-8 -*-
import logging
import urllib
import urllib2

from cookielib import logger
from django.utils import simplejson as json
from .models import NewsItem
from tipfy.app import Response
from tipfy.handler import RequestHandler

logger = logging.getLogger(__name__)

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
