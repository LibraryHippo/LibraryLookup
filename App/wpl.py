#!/usr/bin/env python

def searchUrl(isbn):
    return 'http://books.kpl.org/search~S3/?searchtype=i&searcharg=%(isbn)s&searchscope=3&searchlimits=' % vars()

class Library:
    def __init__(self, opener):
        self.opener = opener

    def has_item(self, isbn):
        response = self.opener(searchUrl(isbn))
        return response.content.find('No matches found') == -1
