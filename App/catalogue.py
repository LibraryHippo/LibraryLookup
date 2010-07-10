#!/usr/bin/env python

import logging

class FindResult:
    def __init__(self, library, url):
        self.library = library
        self.url = url

    def __eq__(self, other):
        return self.library == other.library and self.url == other.url

    def __repr__(self):
        return 'FindResult(' + repr(self.library) + ', ' + self.url + ')'

class Catalogue:
    def __init__(self, xisbn):
        self.xisbn = xisbn

    def find_item(self, isbn, libraries):
        items = []
        for library in libraries:
            logging.debug('looking for ' + isbn)
            url = library.find_item(isbn)
            if url:
                items.append(FindResult(library, url))
            else:
                other_editions = self.xisbn.get_editions(isbn)
                for edition in other_editions:
                    if edition == isbn:
                        continue
                    logging.debug('looking for ' + edition)
                    url = library.find_item(edition)
                    if url:
                        items.append(FindResult(library, url))
                        break
        return items

