#!/usr/bin/env python

import xisbnwebservice
import urllib2


class ContentHolder:
    def __init__(self, content):
        self.content = content


def test_get_editions__10digits__returns_list_of_editions():
    def opener(url): return ContentHolder(urllib2.urlopen(url).read())
    x = xisbnwebservice.XisbnWebService(opener)
    editions = x.get_editions('0316229296')
    assert set([
        u'0316229296',
        u'031622930X',
        u'0356504883',
        u'0356508196',
        u'1478900830',
        u'147895616X',
        u'2290144231',
        u'3426521784',
        u'6050946590',
        u'6068673669',
        u'8592795230',
        u'9634191063',
        u'9780316229296',
        u'9780316229302',
        u'9780356504889',
        u'9780356508191',
        u'9781478900832',
        u'9781478956167',
        u'9782290144237',
        u'9783426521786',
        u'9786050946598',
        u'9786068673660',
        u'9788075775603',
        u'9788379246984',
        u'9788466661690',
        u'9788490697313',
        u'9788592795238',
        u'9789024580439',
        u'9789634191063',
        u'9789896418465',
        u'9789949853298',
    ]).issubset(editions)
