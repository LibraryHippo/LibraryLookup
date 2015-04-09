#!/usr/bin/env python

import library


def search_url(isbn):
    return ('http://www.regionofwaterloo.canlib.ca/uhtbin/cgisirsi/uOtJAQjVct/HEADQUARTR/x/5/0/?searchdata1=%(isbn)s'
            % vars())


class Library(library.LibraryBase):
    def __init__(self, opener):
        self.id = 'rwl'
        self.name = 'Region of Waterloo Library'
        self.opener = opener

    def find_item(self, isbn):
        url = search_url(isbn)
        response = self.opener(url)
        if response.content.find('found no matches in the library you searched') == -1:
            return url
        return None
