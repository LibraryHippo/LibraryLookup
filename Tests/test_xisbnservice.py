#!/usr/bin/env python

import xisbnwebservice

class MyResponse:
    def __init__(self, content, status_code=200, headers={}, final_url='http://www.google.ca/'):
        self.content = content
        self.content_was_truncated = False
        self.status_code=200
        self.headers=headers
        self.final_url=final_url

class MyOpener:
    def __init__(self, *responses):
        self.responses = []
        for response in responses:
            if not isinstance(response, MyResponse):
                response = MyResponse(response)
            self.responses.append(response)

    def __call__(self, url):
        self.last_request = { 'url':url }
        print self.last_request

        response = self.responses.pop(0)
        print 'response', response        
        return response

class MyLibrary:
    def __init__(self):
        self.type = 'MyPL'
        self.name = 'My Public Library'
        
class MyCard:
    def __init__(self):
        self.library = MyLibrary()
        self.name = 'Name'
        self.number = 'Number'
        self.pin = 'pin'

def test_find_synonyms__10digits__makes_good_request():
    opener = MyOpener('')
    x = xisbnwebservice.XisbnWebService(opener)
    x.find_synonyms('0812550706')

    assert 'http://xisbn.worldcat.org/webservices/xid/isbn/0812550706?method=getEditions&format=csv' == opener.last_request['url']

def test_find_synonyms__10digits__returns_list_of_synonyms():
    opener = MyOpener('''0812550706
1593974744
0808586165''')
    x = xisbnwebservice.XisbnWebService(opener)
    synonyms = x.find_synonyms('0812550706')
    assert ['0812550706', '1593974744', '0808586165'] == synonyms

    
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


    
