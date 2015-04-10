#!/usr/bin/env python

import library


def search_url(isbn):
    return ('http://olco.canlib.ca/client/en_US/rwl/search/results?qu=%(isbn)s'
            % vars())


class Library(library.LibraryBase):
    def __init__(self, opener):
        self.id = 'rwl'
        self.name = 'Region of Waterloo Library'
        self.opener = opener

    def find_item(self, isbn):
        url = search_url(isbn)
        response = self.opener(url)
        if response.content.find('This search returned no results.') == -1:
            return url
        return None
