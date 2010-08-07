#!/usr/bin/env python

import library

def searchUrl(isbn):
    return 'http://books.kpl.org/search~S3/?searchtype=i&searcharg=%(isbn)s&searchscope=3&searchlimits=' % vars()

class Library(library.LibraryBase):
    def __init__(self, opener):
        self.id = 'wpl'
        self.name = 'Waterloo Public Library'
        self.opener = opener

    def find_item(self, isbn):
        url = searchUrl(isbn)
        response = self.opener(url)
        if response.content.find('No matches found') == -1:
            return url
        return None
