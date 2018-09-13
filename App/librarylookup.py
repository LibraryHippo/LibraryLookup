#!/usr/bin/env python

import logging
import json

from xml.dom.minidom import Document

from google.appengine.api import urlfetch
import webapp2

import catalogue
import wpl
import dl
import kpl
import rwl
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
    result = ''.join('<li style="background-image: url(http://librarylookup-hrd.appspot.com/static/library_icons/' +
                     f.library.id +
                     '_64.png)"><a href="' +
                     f.url +
                     '">' +
                     f.library.name +
                     '</a></li>\r\n' for f in find_results)

    return '''<html>
<body>
<ul>
''' + result + '''</ul>
</body>
</html>'''


xisbn_web_service = xisbnwebservice.XisbnWebService(urlfetch.fetch)
xisbn_service = xisbn.Xisbn(xisbn_web_service)

catalogue_service = catalogue.Catalogue(xisbn_service)

all_libraries = {
    'wpl': wpl.Library(urlfetch.fetch),
    'kpl': kpl.Library(urlfetch.fetch),
    'rwl': rwl.Library(urlfetch.fetch),
    'dl': dl.Library(urlfetch.fetch),
}


def lookup_isbn_html(isbn, libraries):
    found = catalogue_service.find_item(isbn, libraries)

    return(to_html(found))


class FindIsbn(webapp2.RequestHandler):
    def get(self, isbn):
        request_libraries = self.request.get_all('lib')
        if not request_libraries:
            request_libraries = ['wpl', 'dl', 'kpl', 'rwl']
        logging.debug(request_libraries)
        self.response.headers['Cache-Control'] = 'public; max-age=300;'
        self.response.out.write(lookup_isbn_html(
            isbn, [all_libraries[l] for l in request_libraries]))


class Libraries(webapp2.RequestHandler):
    def get(self):
        libs = {}
        for (key, lib) in all_libraries.iteritems():
            libs[key] = {'name': lib.name}
        self.response.out.write(json.dumps(libs))


logging.getLogger().setLevel(logging.DEBUG)

handlers = [
    ('/isbn/(.*)', FindIsbn),
    ('/libraries', Libraries),
]

application = webapp2.WSGIApplication(handlers, debug=True)
