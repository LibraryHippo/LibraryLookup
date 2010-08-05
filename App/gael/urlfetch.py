#!/usr/bin/env python
'''Extension wrappers for google.appengine.api.urlfetch.

CookieHandler and RedirectFollower use code taken from Scott Hillman's URLOpener
(http://everydayscripting.blogspot.com/2009/08/google-app-engine-cookie-handling-with.html).
'''

import Cookie
import urllib
import urlparse
import datetime


class BaseWrapper:
    '''A base wrapper for creating new wrappers.

    Provides no real functionality other than attribute chaining.
    '''

    def __init__(self, fetcher):
        '''Create a new wrapped fetcher.

        Will use the fetcher parameter to actually perform queries.
        '''
        self.fetcher = fetcher

    def __getattr__(self, name):
        '''Ensures that any attribute defined on a wrapped fetcher is available on the wrapper.'''
        return getattr(self.fetcher, name)

class CookieHandler(BaseWrapper):
    '''A fetcher that stores and provides cookies
    '''
    
    def __init__(self, fetcher):
        '''Create a new wrapped fetcher.

        Will use the fetcher parameter to actually perform queries.
        '''
        BaseWrapper.__init__(self, fetcher)
        self.cookie_jar = Cookie.SimpleCookie()

    def __call__(self, url, payload=None, method='GET', headers={},
                 allow_truncated=False, follow_redirects=True, deadline=None):
        '''Fetch, keeping track of all cookies
        '''
        headers['Cookie'] = self._make_cookie_header()
        response = self.fetcher(url, payload, method, headers,
                                allow_truncated, follow_redirects, deadline)
        self.cookie_jar.load(response.headers.get('set-cookie', ''))
        return response
    
    def _make_cookie_header(self):
        cookieHeader = ""
        for value in self.cookie_jar.values():
            cookieHeader += "%s=%s; " % (value.key, value.value)
        return cookieHeader

class RedirectFollower(BaseWrapper):
    '''A fetcher that follows all redirects.
    '''
    def __call__(self, url, payload=None, method='GET', headers={},
                 allow_truncated=False, follow_redirects=False, deadline=None):
        '''Fetch, following all redirects

        Sets follow_redirects to False. After the first query, method will be set to GET.
        '''
        while True:
            response = self.fetcher(url, payload, method, headers,
                                    allow_truncated, False, deadline)
            new_url = response.headers.get('location')
            if new_url:
                # Join the URLs in case the new location is relative
                url = urlparse.urljoin(url, new_url)

                # Next request should be a get, payload needed
                method = 'GET'
                payload = None
            else:
                break

        return response

class PayloadEncoder(BaseWrapper):
    '''A fetcher that automatically encodes its payload argument.
    '''
    def __call__(self, url, payload=None, method='GET', headers={}, allow_truncated=False, follow_redirects=True, deadline=None):
        '''Fetch, after encoding the payload argument

        If payload is not None, method will be set to POST.
        '''
        if payload is not None:
            method = 'POST'
            payload = urllib.urlencode(payload)
        return self.fetcher(url, payload, method, headers, allow_truncated, follow_redirects, deadline)

class Transcriber(BaseWrapper):
    '''A fetcher that maintains a record of all its requests and responses.'''
    def __init__(self, fetcher):
        '''Create a new wrapped fetcher.

        Will use the fetcher parameter to actually perform queries.
        '''
        BaseWrapper.__init__(self, fetcher)
        self. transactions = []

    def __call__(self, url, payload=None, method='GET', headers={}, allow_truncated=False, follow_redirects=True, deadline=None):
        '''Fetch, recording transactions

        Later, transactions may be retrieved from the transactions attribute.
        '''
        self.transactions.append(Transcriber._Request(vars()))
        response = self.fetcher(url, payload, method, headers, allow_truncated, follow_redirects, deadline)
        self.transactions.append(Transcriber._Response(response))
        return response

    class _Request:
        def __init__(self, values):
            self.values = dict((key, values[key])
                               for key in ('url', 'method', 'payload', 'headers'))
            self.values['time'] = datetime.datetime.now()

        def __str__(self):
            return '''Request at %(time)s:
  url = %(url)s
  method = %(method)s
  payload = %(payload)s
  headers = %(headers)s''' % self.values

    class _Response:
        def __init__(self, values):
            self.values = dict(status_code=values.status_code,
                               headers=values.headers,
                               content=values.content,
                               time=datetime.datetime.now())

        def __str__(self):
            return '''Response at %(time)s:
  status_code = %(status_code)d
  headers = %(headers)s
  content = %(content)s''' % self.values
