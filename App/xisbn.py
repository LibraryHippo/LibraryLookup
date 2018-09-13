#!/usr/bin/env python

from gael import memcache


class Xisbn:
    def __init__(self, source):
        self.xisbn_source = source

    @memcache.memoize(lambda args, kwargs: args[1], 3600)
    def find_editions(self, isbn):
        return self.xisbn_source.get_editions(isbn)
