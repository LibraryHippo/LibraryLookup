#!/usr/bin/env python

import xisbn

from fakes import MyXisbnWebService


def test_get_editions__isbn10_no_13s__returns_isbn10_synonyms_and_single_13():
    web_service = MyXisbnWebService()
    web_service['1234567890'] = ['3820967206', '398465451X', '8465416954']
    x = xisbn.Xisbn(web_service)

    editions = x.get_editions('1234567890')

    assert '1234567890' in editions
    assert '3820967206' in editions
    assert '398465451X' in editions
    assert '8465416954' in editions
    assert '1234567890147' in editions


def test_get_editions__isbn13_no_10s__returns_isbn13_synonyms_and_single_10():
    web_service = MyXisbnWebService()
    web_service['1212334567890'] = ['3845620967206', '378998465451X', '8461595416954']
    x = xisbn.Xisbn(web_service)

    editions = x.get_editions('1212334567890')

    assert '1212334567890' in editions
    assert '3845620967206' in editions
    assert '378998465451X' in editions
    assert '8461595416954' in editions
    assert '2334567890' in editions
