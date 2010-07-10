#!/usr/bin/env python

import sys
import logging

from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import catalogue
import wpl
import kpl
import xisbn
import xisbnwebservice

class FindIsbn(webapp.RequestHandler):
    def __init__(self):
        
        xisbn_web_service = xisbnwebservice.XisbnWebService(urlfetch.fetch)
        xisbn_service = xisbn.Xisbn(xisbn_web_service)

        self.catalogue_service = catalogue.Catalogue(xisbn_service)

    def get(self, isbn):
        #logging.debug('path = ', self.request.path)
        logging.debug('path = ' + str(dir(self)))

        libraries = [wpl.Library(urlfetch.fetch),
                   kpl.Library(urlfetch.fetch)]
        self.response.out.write('<html><body><ul>\n')
        found = self.catalogue_service.find_item(isbn, libraries)
        self.response.out.write('searching for ' + isbn + '\n')
        for f in found:
            self.response.out.write('<li><a href="' + str(f.url) + '">' + str(f.library.name) + '</a></li>\n')
        self.response.out.write('</ul></body><html>\n')
        

def main(handlers=[]):
    logging.getLogger().setLevel(logging.DEBUG)

    if not handlers:
        handlers.extend([
            ('/isbn/(.*)', FindIsbn),
            ])

    application = webapp.WSGIApplication(
        handlers,
        debug=False)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()

