#!/usr/bin/env python

import catalogue

class MyLibrary:
    def __init__(self):
        self. holdings = []

    def has(self, isbn):
        self.holdings.append(isbn)

    def find_item(self, isbn):
        if isbn in self.holdings:
            return ('MyLibrary', 'http://my.lib/' + isbn)
        return None

class MyXisbn:
    def __init__(self):
        self.edition_map = {}

    def __setitem__(self, isbn, alternates):
        self.edition_map[isbn] = [isbn] + alternates

    def get_editions(self, isbn):
        if isbn in self.edition_map:
            return self.edition_map[isbn]
        return [isbn]


def test_find_item__single_library_item_there__finds_item():
    x = MyXisbn()
    l = MyLibrary()
    l.has('1234516591')

    c = catalogue.Catalogue(x)

    found_items = c.find_item('1234516591', [l])

    assert found_items == ('MyLibrary', 'http://my.lib/1234516591')

def test_find_item__single_library_other_edition_there__finds_item():
    x = MyXisbn()
    x['1234516591'] = ['1234516592']

    l = MyLibrary()
    l.has('1234516592')

    c = catalogue.Catalogue(x)

    found_items = c.find_item('1234516591', [l])

    assert found_items == ('MyLibrary', 'http://my.lib/1234516592')


