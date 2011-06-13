# -*- coding: utf-8 -*-
import logging
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
      created_from = 'NOW-35MINUTES'
      #created_from = 'NOW-3HOURS'
      created_to = 'NOW'
      logging.info("Polling HNSearchAPI from %s to %s " % (created_from, created_to))
      result = api.search(created_from=created_from, created_to=created_to, start=0, limit=0)
      content = json.loads(result, encoding="utf-8")
      hits = int(content['hits'])
      logger.info("Got %s hnsearch hits" % content['hits'])
      if hits > 1000:
        hits = 1000
        logger.warn("Number of hits is over limit. Trimming to 1000")
      for start in xrange(0, hits, limit):
        taskname = "poll-hnsearch-%s-%s" % (created_from, created_to)
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
    items = NewsItem.all(keys_only=True).filter("is_sentiment_processed", False).filter("is_sentiment_queued", False).order('-create_ts').fetch(limit=100)
    for key in items:
      keyname = key.name()
      # queue sentiment analisys task
      taskname = "sentimental-analisys-%s" % keyname
      task = taskqueue.Task(params={'itemid':keyname}, name=taskname, method="GET", url="/tasks/poll_alchemyapi")
      queue.add(task)
      logger.info("Created task %s" % taskname)
      # set item as queue
      newsitem = NewsItem.get_by_key_name(keyname)
      newsitem.is_sentiment_queued = True
      newsitem.put()
    return Response('OK', status=200)