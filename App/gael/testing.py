import sys


def add_appsever_import_paths():
    from dev_appserver import EXTRA_PATHS
    for extra_path in EXTRA_PATHS:
        if extra_path not in sys.path:
            sys.path = [extra_path] + sys.path


add_appsever_import_paths()

import google.appengine.ext.testbed  # noqa402
import google.appengine.api.memcache  # noqa402


def setup_memcache():
    my_testbed = google.appengine.ext.testbed.Testbed()
    my_testbed.activate()
    my_testbed.init_memcache_stub()


def flush_memcache():
    google.appengine.api.memcache.flush_all()
