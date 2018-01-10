#!/usr/bin/env python

import library


def search_url(isbn):
    return 'https://downloadlibrary.overdrive.com/search/title?isbn=%(isbn)s' % vars()


class Library(library.LibraryBase):
    def __init__(self, opener):
        self.id = 'dl'
        self.name = 'Download Library'
        self.opener = opener

    def find_item(self, isbn):
        url = search_url(isbn)
        response = self.opener(url)
        if 'We couldn&#39;t find any matches for your search.' in response.content:
            return None
        return url
