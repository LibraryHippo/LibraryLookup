#!/usr/bin/env python

from fakes import MyOpener
import wpl

import os

def load_file(filename):
    return file(os.path.join(os.path.dirname(__file__), filename)).read()

def test_find_item__isbn10__makes_good_request():
    opener = MyOpener('')
    w = wpl.Library(opener)

    w.find_item('1593974744')
    assert opener.last_request['url'] == 'http://books.kpl.org/search~S3/?searchtype=i&searcharg=1593974744&searchscope=3&searchlimits='

def test_find_item__isbn10_in_library__returns_record():
    opener = MyOpener(load_file('wpl_has_item.html'))
    w = wpl.Library(opener)

    record =  w.find_item('1593974744')
    assert record == ('Waterloo Public Library', 'http://books.kpl.org/search~S3/?searchtype=i&searcharg=1593974744&searchscope=3&searchlimits=')

def test_find_item__isbn10_not_in_library__returns_false():
    opener = MyOpener(load_file('wpl_has_not_item.html'))
    w = wpl.Library(opener)

    has = w.find_item('0321125215')
    assert not has
