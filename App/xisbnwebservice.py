#!/usr/bin/env python


def method_url(method, isbn):
    return 'http://xisbn.worldcat.org/webservices/xid/isbn/%(isbn)s?method=%(method)s&format=csv' % vars()


class XisbnWebService:
    def __init__(self, opener):
        self.opener = opener

    def get_editions(self, isbn):
        response = self.opener(method_url('getEditions', isbn)).content
        return response.split()

    def to13(self, isbn10):
        response = self.opener(method_url('to13', isbn10)).content
        return response.strip()

    def to10(self, isbn13):
        response = self.opener(method_url('to10', isbn13)).content
        return response.strip()
