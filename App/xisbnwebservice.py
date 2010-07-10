#!/usr/bin/env python

import logging
from google.appengine.api import urlfetch

def methodUrl(method, isbn):
    return 'http://xisbn.worldcat.org/webservices/xid/isbn/%(isbn)s?method=%(method)s&format=csv' % vars()

class XisbnWebService:
    def __init__(self, opener):
        self.opener = opener

    def get_editions(self, isbn):
        response = self.opener(methodUrl('getEditions', isbn)).content
        return response.split()

    def to13(self, isbn10):
        response = self.opener(methodUrl('to13', isbn10)).content
        return response.strip()

    def to10(self, isbn13):
        response = self.opener(methodUrl('to10', isbn13)).content
        return response.strip()

if __name__ == '__main__':

    class Opener:
        def __call__(self, url):
            class Result:
                pass
            
            r = Result()
            r.content = urllib2.urlopen(url).read()
            return r
            
    import urllib2
    import sys
    import gael.testing
    gael.testing.add_appsever_import_paths()
    gael.testing.initialize_service_apis()
    
    opener = Opener()
    x = XisbnWebService(urlfetch.fetch)
    print x.get_editions(sys.argv[1])
