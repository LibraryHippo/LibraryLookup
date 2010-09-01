#!/usr/bin/env python

import library

def searchUrl(isbn):
    return 'http://books.kpl.org/search~S2/?searchtype=i&searcharg=%(isbn)s&searchlimits=&searchscope=2' % vars()

class Library(library.LibraryBase):
    def __init__(self, opener):
        self.id = 'kpl'
        self.name = 'Kitchencher Public Library'
        self.opener = opener

    def find_item(self, isbn):
        url = searchUrl(isbn)
        response = self.opener(url)
        if response.content.find('No matches found') == -1:
            return url
        return None
