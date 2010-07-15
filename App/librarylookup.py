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
import xisbn
import xisbnwebservice

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
        
class FindIsbn(webapp.RequestHandler):
    def __init__(self):
        
        xisbn_web_service = xisbnwebservice.XisbnWebService(urlfetch.fetch)
        xisbn_service = xisbn.Xisbn(xisbn_web_service)

        self.catalogue_service = catalogue.Catalogue(xisbn_service)

    def get(self, isbn):
        libraries = [wpl.Library(urlfetch.fetch),
                   kpl.Library(urlfetch.fetch)]
        found = self.catalogue_service.find_item(isbn, libraries)

        #self.response.headers['Content-Type'] = "application/xml"
        self.response.out.write(to_html(found))

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

