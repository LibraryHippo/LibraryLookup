#!/usr/bin/env python

from gael import memcache


class Xisbn:
    def __init__(self, source):
        self.xisbn_source = source

    @memcache.memoize(lambda args, kwargs: args[1], 3600)
    def find_editions(self, isbn):
        editions = self.xisbn_source.get_editions(isbn)
        if len(isbn) == 13:
            isbn10 = self.xisbn_source.to10(isbn)
            editions += self.xisbn_source.get_editions(isbn10)
        elif len(isbn) == 10:
            isbn13 = self.xisbn_source.to13(isbn)
            editions += self.xisbn_source.get_editions(isbn13)
        return editions
