#!/usr/bin/env python

import sys
import logging

from xml.dom.minidom import Document

from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import catalogue
import wpl
import kpl
import rwl
import xisbn
import xisbnwebservice
from gael import memcache

def to_xml(find_results):
    doc = Document()
    foundisbns = doc.createElement("foundisbns")
    doc.appendChild(foundisbns)

    for f in find_results:
        foundisbn = doc.createElement("foundisbn")

        library = doc.createElement('library')
        library.appendChild(doc.createTextNode(f.library.name))
        foundisbn.appendChild(library)

        url = doc.createElement('url')
        url.appendChild(doc.createTextNode(f.url))
        foundisbn.appendChild(url)

        foundisbns.appendChild(foundisbn)

    return doc.toprettyxml(indent="  ")

def to_html(find_results):
    result = ''.join('<li><a href="' + f.url + '">' + f.library.name + '</a></li>\r\n'
                     for f in find_results)

    return '''<html>
<body>
<ul>
''' + result  + '''</ul>
</body>
</html>'''

xisbn_web_service = xisbnwebservice.XisbnWebService(urlfetch.fetch)
xisbn_service = xisbn.Xisbn(xisbn_web_service)

catalogue_service = catalogue.Catalogue(xisbn_service)

libraries = [wpl.Library(urlfetch.fetch), kpl.Library(urlfetch.fetch), rwl.Library(urlfetch.fetch)]

@memcache.memoize(lambda args, kwargs: args[0], 3600)
def lookup_isbn_html(isbn):
        found = catalogue_service.find_item(isbn, libraries)

        #self.response.headers['Content-Type'] = "application/xml"
        return(to_html(found))
    
    

class FindIsbn(webapp.RequestHandler):
    def get(self, isbn):
        self.response.out.write(lookup_isbn_html(isbn))

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

