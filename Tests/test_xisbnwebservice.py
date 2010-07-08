#!/usr/bin/env python

from fakes import MyOpener
import xisbnwebservice

def test_get_editions__10digits__makes_good_request():
    opener = MyOpener('')
    x = xisbnwebservice.XisbnWebService(opener)
    x.get_editions('0812550706')

    assert 'http://xisbn.worldcat.org/webservices/xid/isbn/0812550706?method=getEditions&format=csv' == opener.last_request['url']

def test_get_editions__10digits__returns_list_of_editions():
    opener = MyOpener('''0812550706
1593974744
0808586165''')
    x = xisbnwebservice.XisbnWebService(opener)
    editions = x.get_editions('0812550706')
    assert ['0812550706', '1593974744', '0808586165'] == editions

    
def test_to13__10digits__makes_good_request():
    opener = MyOpener('')
    x = xisbnwebservice.XisbnWebService(opener)
    x.to13('0596002815')

    assert 'http://xisbn.worldcat.org/webservices/xid/isbn/0596002815?method=to13&format=csv' == opener.last_request['url']

def test_to13__10digits__finds_good_alternate():
    opener = MyOpener('9780596002817')
    x = xisbnwebservice.XisbnWebService(opener)
    assert '9780596002817' == x.to13('0596002815')

def test_to10__13digits__makes_good_request():
    opener = MyOpener('')
    x = xisbnwebservice.XisbnWebService(opener)
    x.to10('0596002815')

    assert 'http://xisbn.worldcat.org/webservices/xid/isbn/0596002815?method=to10&format=csv' == opener.last_request['url']

def test_to10__13digits__finds_good_alternate():
    opener = MyOpener('0596002815')
    x = xisbnwebservice.XisbnWebService(opener)
    assert '0596002815' == x.to10('9780596002817')


    
