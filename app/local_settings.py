'''
'''
import os

if os.environ.get('SERVER_SOFTWARE', '').startswith('Dev'):
  ALCHEMY_API_KEY='58fbb0bcc99e5a7c9160b2a23fcedbea16c92a01' #zemanel@maybeitworks.com
else:
  ALCHEMY_API_KEY='dd804ff71af6a6e01e7c35667f2dcfe3413a99e5' #zemanel@zemanel.eu

