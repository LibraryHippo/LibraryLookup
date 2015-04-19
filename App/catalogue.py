#!/usr/bin/env python

import logging
from gael import memcache


class FindResult:
    def __init__(self, library, url):
        self.library = library
        self.url = url

    def __eq__(self, other):
        return self.library == other.library and self.url == other.url

    def __repr__(self):
        return 'FindResult(' + repr(self.library) + ', ' + self.url + ')'


@memcache.memoize(lambda args, kwargs: repr(args), 3600)
def find(library, isbn):
    result = library.find_item(isbn)
    return result or 'NOTFOUND'


class Catalogue:
    def __init__(self, xisbn):
        self.xisbn = xisbn

    def find_item(self, isbn, libraries):
        items = []
        for library in libraries:
            items_found_so_far = len(items)
            logging.debug('looking for ' + isbn + ' in ' + library.name)
            url = find(library, isbn)
            if url != 'NOTFOUND':
                logging.info('found ' + isbn + ' in ' + library.name)
                items.append(FindResult(library, url))
            else:
                other_editions = self.xisbn.get_editions(isbn)
                for edition in other_editions:
                    if edition == isbn:
                        continue
                    logging.debug('looking for ' + edition + ' in ' + library.name)
                    url = find(library, edition)
                    if url != 'NOTFOUND':
                        logging.info('found ' + edition + ' in ' + library.name)
                        items.append(FindResult(library, url))
                        break
            if len(items) == items_found_so_far:
                logging.info('could not find ' + isbn + ' in ' + library.name)
        return items
