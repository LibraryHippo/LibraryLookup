#!/usr/bin/env python

from gael import memcache


@memcache.memoize(lambda args, kwargs: args[1], 3600)
def find_editions(xisbn_source, isbn):
    editions = xisbn_source.get_editions(isbn)
    if len(isbn) == 13:
        isbn10 = xisbn_source.to10(isbn)
        editions += xisbn_source.get_editions(isbn10)
    elif len(isbn) == 10:
        isbn13 = xisbn_source.to13(isbn)
        editions += xisbn_source.get_editions(isbn13)
    return editions


class Xisbn:
    def __init__(self, source):
        self.xisbn_source = source

    def get_editions(self, isbn):
        return find_editions(self.xisbn_source, isbn)
