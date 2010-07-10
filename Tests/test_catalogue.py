#!/usr/bin/env python

import catalogue

class MyLibrary:
    def __init__(self, name='MyLibrary'):
        self.name = name
        self. holdings = []

    def has(self, isbn):
        self.holdings.append(isbn)

    def find_item(self, isbn):
        if isbn in self.holdings:
            return 'http://my.lib/' + isbn
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

    assert catalogue.FindResult(l, 'http://my.ldib/1234516591') in found_items

def test_find_item__single_library_item_not_there__does_not_find_item():
    x = MyXisbn()
    l = MyLibrary()
    l.has('1234516591')

    c = catalogue.Catalogue(x)

    found_items = c.find_item('3234514591', [l])

    assert found_items == []

def test_find_item__single_library_other_edition_there__finds_item():
    x = MyXisbn()
    x['1234516591'] = ['1234516592']

    l = MyLibrary()
    l.has('1234516592')

    c = catalogue.Catalogue(x)

    found_items = c.find_item('1234516591', [l])

    assert catalogue.FindResult(l, 'http://my.lib/1234516592') in found_items


def test_find_item__single_library_two_editions_there__finds_original():
    x = MyXisbn()
    x['1234516591'] = ['1234516592']

    l = MyLibrary()
    l.has('1234516591')
    l.has('1234516592')    

    c = catalogue.Catalogue(x)

    found_items = c.find_item('1234516592', [l])

    assert [catalogue.FindResult(l, 'http://my.lib/1234516592')] == found_items


def test_find_item__two_libraries_item_in_both__finds_both():
    x = MyXisbn()

    l1= MyLibrary('MyLibrary1')
    l1.has('1234516591')

    l2 = MyLibrary('MyLibrary2')
    l2.has('1234516591')

    c = catalogue.Catalogue(x)

    found_items = c.find_item('1234516591', [l1, l2])

    assert catalogue.FindResult(l1, 'http://my.lib/1234516591') in found_items
    assert catalogue.FindResult(l2, 'http://my.lib/1234516591') in found_items


