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
from .hnsearchapi import HNSearchAPI

logger = logging.getLogger(__name__)

class QueueHNSearchJob(RequestHandler):
  def get(self):
    '''Poll HNSearch API for news comments
    '''
    queue = taskqueue.Queue(name='hnsearchapi')
    api = HNSearchAPI()
    limit=100
    try:
      #result = api.search(created_from='NOW-30MINUTES', created_to='NOW', limit=100)
      created_from = 'NOW-30MINUTES'
      created_to = 'NOW'
      result = api.search(created_from=created_from, created_to=created_to, start=0, limit=0)
      content = json.loads(result, encoding="utf-8")
      hits = int(content['hits'])
      logger.info("Got %s hnsearch hits" % content['hits'])
      for start in xrange(0, hits, limit):
        taskname = "poll-hnsearch-%s" % (start)
        params = {
          'created_from' : created_from,
          'created_to' : created_to,
          'start' : start,
          'limit' : limit,
        }
        task = taskqueue.Task(params=params, name=taskname, method="GET", url="/tasks/poll_hnsearch")
        queue.add(task)
        logging.info("Created task %s" % taskname)
    except Exception, e:
      logger.exception(e)
      self.abort(500)
    return Response('OK', status=200)



class QueueAlchemyTasksJob(RequestHandler):
  def get(self):
    '''Fills a GAP task queue with items sentiment analisys
    '''
    queue = taskqueue.Queue(name='alchemyapi')
    items = NewsItem.all(keys_only=True).filter("is_sentiment_processed", False).order('-create_ts').fetch(limit=100)
    for key in items:
      keyname = key.name()
      taskname = "sentimental-analisys-%s" % keyname
      task = taskqueue.Task(params={'itemid':keyname}, name=taskname, method="GET", url="/tasks/poll_alchemyapi")
      queue.add(task)
      logger.info("Created task %s" % taskname)
    return Response('OK', status=200)