# -*- coding: utf-8 -*-
import logging
import urllib
import urllib2
import datetime

from django.utils import simplejson as json
from tipfy.app import Response
from tipfy.handler import RequestHandler
from google.appengine.api import taskqueue

from .models import NewsItem

logger = logging.getLogger(__name__)

class PollHNSearchJob(RequestHandler):
  def get(self):
    '''Poll HNSearch API for news comments
    '''
    try:
      self._request_results()
    except Exception, e:
      logger.exception(e)
      self.abort(500)
    return Response('OK', status=200)

  def _request_results(self, start=0, limit=100, pretty_print=True):
    '''
    '''
    baseurl = "http://api.thriftdb.com/api.hnsearch.com/items/_search?"
    params = {
      'filter[fields][type]' : 'comment',
      'filter[fields][create_ts]' : '[NOW-30MINUTES TO NOW]',
      'sortby' : 'create_ts desc',
      'start' : start,
      'limit' : limit,
      'pretty_print': pretty_print
    }
    result = urllib2.urlopen(baseurl + urllib.urlencode(params))
    content = json.loads(result.read(), encoding="utf-8")
    self._parse_results(content['results'])

  def _parse_results(self, results):
    '''stores news items in the datastore
    '''
    for item in results:
      key = str(item['item']['id'])
      logger.debug(item)
      props = {
        'text' : item['item']['text'],
        'username' : item['item']['username'],
        'type': item['item']['type'],
        'create_ts' : datetime.datetime.strptime(item['item']['create_ts'], '%Y-%m-%dT%H:%M:%SZ'),
        'parent_id' : int(item['item']['parent_id'])
      }
      NewsItem.get_or_insert(key_name=key, **props)
      logger.info("Stored item %s" % key)

class QueueAlchemyTasksJob(RequestHandler):
  def get(self):
    '''Fills a GAP task queue with items sentiment analisys
    '''
    queue = taskqueue.Queue()
    items = NewsItem.all(keys_only=True).filter("is_sentiment_processed", False).order('-created_on').fetch(limit=100)
    for key in items:
      keyname = key.name()
      taskname = "sentimental-analisys-%s" % keyname
      task = taskqueue.Task(params={'itemid':keyname}, name=taskname, method="GET", url="/tasks/poll_alchemyapi")
      queue.add(task)
      logger.info("Created task %s" % taskname)
    return Response('OK', status=200)