#!/usr/bin/env python

import logging
import google.appengine.api.memcache


def memoize(key, seconds_to_keep=600):
    '''Use the memcache to memoize a callable's results. Returns a
    function that will check to see if a result is stored in the
    memcache. If not, it will call the original function and store the
    result in the memcache for seconds_to_keep seconds. The key used
    to identify the results in the memcache is equal to
    key_func(*args, **kwargs), where *args and **kwargs are the
    arguments to the decorated function.
    ''' 
    class memoize():
        def __init__(self, func):
            self.key = key
            self.seconds_to_keep=600
            self.func = func
            self.cache=google.appengine.api.memcache

        def __call__(self, *args, **kwargs):
            if callable(self.key):
                key_value = self.key(args, kwargs)
            else:
                key_value = self.key % kwargs

            cached_result = self.cache.get(key_value)
            if cached_result is not None:
                logging.debug('found ' + key_value)
                return cached_result
            logging.info('calling func to get '  + key_value)
            result = self.func(*args, **kwargs)

            self.cache.set(key_value, result, self.seconds_to_keep)
            return result

    return memoize
