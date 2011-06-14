# -*- coding: utf-8 -*-
import logging
import rfc3339
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
            now = datetime.datetime.now()
            now_rfc = rfc3339.rfc3339(now, utc=True)
            created_from = "%s-10MINUTES" % now_rfc
            created_to = now_rfc
            logging.info("Polling HNSearchAPI from %s to %s " % (created_from, created_to))
            result = api.search(created_from=created_from, created_to=created_to, start=0, limit=0)
            content = json.loads(result, encoding="utf-8")
            hits = int(content['hits'])
            logger.info("Got %s hnsearch hits" % content['hits'])
            if hits > 1000:
                hits = 1000
                logger.warn("Number of hits is over limit. Trimming to 1000")
            for start in xrange(0, hits, limit):
                #taskname = "poll-hnsearch-%s-%s" % (created_from, created_to)
                params = {
                    'created_from' : created_from,
                    'created_to' : created_to,
                    'start' : start,
                    'limit' : limit,
                }
                task = taskqueue.Task(params=params, method="GET", url="/tasks/poll_hnsearch")
                queue.add(task)
                logging.info("Created task %s" % task.name)
        except Exception, e:
            logger.exception(e)
            self.abort(500)
        return Response('OK', status=200)


class QueueAlchemyTasksJob(RequestHandler):
    def get(self):
        '''Fills a GAP task queue with items sentiment analysis
        '''
        queue = taskqueue.Queue(name='alchemyapi')
        #items = NewsItem.all(keys_only=True).filter("is_sentiment_processed", False).filter("is_sentiment_queued", False).order('-create_ts').fetch(limit=100)
        items = NewsItem.all(keys_only=True).filter("is_sentiment_processed", False).order('-create_ts').fetch(limit=100)
        for key in items:
            keyname = key.name()
            # queue sentiment analysis task
            taskname = "sentimental-analysis-%s" % keyname
            task = taskqueue.Task(params={'itemid':keyname}, name=taskname, method="GET", url="/tasks/poll_alchemyapi")
            queue.add(task)
            logger.info("Created task %s" % taskname)
            # set item as queue
            newsitem = NewsItem.get_by_key_name(keyname)
            newsitem.is_sentiment_queued = True
            newsitem.put()
        return Response('OK', status=200)
        
        
class SchemaMigration(RequestHandler):
    def get(self):
        '''Fills a GAP task queue with items sentiment analysis
        '''
        queue = taskqueue.Queue(name='default')