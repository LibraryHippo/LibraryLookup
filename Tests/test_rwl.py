#!/usr/bin/env python

from fakes import MyOpener
import rwl

import os


def load_file(filename):
    return file(os.path.join(os.path.dirname(__file__), filename)).read()


def test_find_item__isbn10__makes_good_request():
    opener = MyOpener('')
    w = rwl.Library(opener)

    w.find_item('0060515198')
    assert (opener.last_request['url'] ==
            'http://www.regionofwaterloo.canlib.ca/uhtbin/cgisirsi/uOtJAQjVct/HEADQUARTR/x/5/0/?searchdata1=0060515198')


def test_find_item__isbn10_in_library__returns_record():
    opener = MyOpener(load_file('rwl_has_item.html'))
    w = rwl.Library(opener)

    record = w.find_item('0060515198')
    assert (record ==
            'http://www.regionofwaterloo.canlib.ca/uhtbin/cgisirsi/uOtJAQjVct/HEADQUARTR/x/5/0/?searchdata1=0060515198')


def test_find_item__isbn10_not_in_library__returns_false():
    opener = MyOpener(load_file('rwl_has_not_item.html'))
    w = rwl.Library(opener)

    has = w.find_item('0321503627')
    assert not has
