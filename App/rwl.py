#!/usr/bin/env python

def searchUrl(isbn):
    return 'http://www.regionofwaterloo.canlib.ca/uhtbin/cgisirsi/uOtJAQjVct/HEADQUARTR/x/5/0/?searchdata1=%(isbn)s' % vars()

class Library:
    def __init__(self, opener):
        self.name = 'Region of Waterloo Library'
        self.opener = opener

    def find_item(self, isbn):
        url = searchUrl(isbn)
        response = self.opener(url)
        if response.content.find('found no matches in the library you searched') == -1:
            return url
        return None
