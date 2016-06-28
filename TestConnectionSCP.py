###############################################################################
#
# $Id: TestConnectionSCP.py 5173 2016-06-28 17:09:03Z rollingcircle $
# 
#
# Debug SemiAutomaticClassificationPlugin connection issue

###############################################################################

def dl(asMsg):
  print("TestConnectionSCP.py : " + asMsg)

import requests
import ssl

dl("ssl.OPENSSL_VERSION = %s" % ssl.OPENSSL_VERSION)


from functools import wraps

#
# Available SSL versions in Python 2.7
#
"""
[ 'PROTOCOL_SSLv2'
, 'PROTOCOL_SSLv23'
, 'PROTOCOL_SSLv3'
, 'PROTOCOL_TLSv1'
]
"""

def sslwrap(func):
  dl("sslwrap() [INIT]")
  dl("func = %s" % func)
  
  @wraps(func)
  def sslwrap_inner(*args, **kw):
    dl("sslwrap_inner() [INIT]")
    dl("args = %s"  % str(args))
    dl("kw = %s"  % str(kw))
    
    #
    # Apply specific SSL version here.
    #
    kw['ssl_version'] = ssl.PROTOCOL_TLSv1 # ssl.PROTOCOL_TLSv1
    
    dl("kw = %s"  % str(kw))
    
    loRC = func(*args, **kw)
    
    dl("sslwrap_inner() [EXIT] : %s" % str(loRC))
    return loRC
  
  dl("sslwrap() [EXIT] : %s" % sslwrap_inner)
  return sslwrap_inner

#ssl.wrap_socket = sslwrap(ssl.wrap_socket)


import urllib2
import sys

def main():
  dl("main() [INIT]")
  
  lsUser = "test"
  
  lsPass = "test"
  
  lsProtocol = 'https:'
  
  lsURL = lsProtocol + '//scihub.copernicus.eu/s2/search?q=S2A*%20AND%20beginPosition:[2014-01-01T00:00:00.000Z%20TO%202016-06-19T23:59:59.999Z]%20AND%20footprint:"Intersects%28POLYGON%28%28-3.09963393869%2052.4131807082,-3.09963393869%2051.3637528892,-1.45348156526%2051.3637528892,-1.45348156526%2052.4131807082,-3.09963393869%2052.4131807082%29%29%29%22'

  lsTopLevelURL = lsProtocol + '//scihub.copernicus.eu'
  
  loPasswdMgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
  dl("loPasswdMgr = %s" % loPasswdMgr)
  
  loPasswdMgr.add_password( None
                          , lsTopLevelURL
                          , lsUser.encode(sys.getfilesystemencoding())
                          , lsPass.encode(sys.getfilesystemencoding())
                          )
  
  loHandler = urllib2.HTTPBasicAuthHandler(loPasswdMgr)
  dl("loHandler = %s" % loHandler)
  
  loOpener = urllib2.build_opener(loHandler)
  dl("loOpener = %s" % loOpener)
  
  dl('lsURL = %s ' % lsURL)
  loResponse = loOpener.open(lsURL)
  dl("loResponse = %s" % loResponse)
  
  dl("main() [EXIT]")
  
##############################################################################

if __name__ == '__main__':
  main()