'''
'''
import urllib
import urllib2
import logging

logger = logging.getLogger(__name__)

class HNSearchAPI(object):
  
  baseurl = "http://api.thriftdb.com/api.hnsearch.com/items/_search?"
  
  def search(self, created_from, created_to, start=0, limit=100, pretty_print=True, sort_by='create_ts desc'):
    '''Performs a request to HNSearch
    '''
    params = {
      'filter[fields][type]' : 'comment',
      'filter[fields][create_ts]' : '[%s TO %s]' % (created_from, created_to),
      'sortby' : sort_by,
      'start' : start,
      'limit' : limit,
      'pretty_print': pretty_print
    }
    url = self.baseurl + urllib.urlencode(params)
    logger.info("Fetching url %s" % url)
    result = urllib2.urlopen(url)
    return result.read()
    