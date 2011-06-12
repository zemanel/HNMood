'''
'''
import urllib
import urllib2

class AlchemyAPI(object):
  
  baseurl = "http://access.alchemyapi.com/calls/text/TextGetTextSentiment"
  
  def __init__(self, apikey):
    self.apikey=apikey
  
  def request(self, text, outputMode='json'):
    '''Performs a request
    '''
    result = urllib2.urlopen(self.baseurl, urllib.urlencode({
      'apikey' : self.apikey,
      'outputMode' : outputMode,
      'text' :  text
    }))
    return result.read()
    