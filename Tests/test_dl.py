#!/usr/bin/env python

import fakes
import dl
import os


def load_file(filename):
    return file(os.path.join(os.path.dirname(__file__), filename)).read()


def test_find_item__isbn13__makes_good_request():
    opener = fakes.MyOpener('')
    w = dl.Library(opener)

    w.find_item('9781250158079')
    assert (opener.last_request['url'] ==
            'https://downloadlibrary.overdrive.com/search/title?isbn=9781250158079')


def test_find_item__isbn13_in_library__returns_record():
    opener = fakes.MyOpener(load_file('dl_has_item.html'))
    w = dl.Library(opener)

    record = w.find_item('9781250158079')
    assert record == 'https://downloadlibrary.overdrive.com/search/title?isbn=9781250158079'


def test_find_item__isbn13_not_in_library__returns_false():
    opener = fakes.MyOpener(load_file('dl_has_not_item.html'))
    w = dl.Library(opener)

    has = w.find_item('9781250158078')
    assert not has
