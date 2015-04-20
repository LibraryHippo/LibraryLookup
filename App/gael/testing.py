import sys


def add_appsever_import_paths():
    from dev_appserver import EXTRA_PATHS
    for extra_path in EXTRA_PATHS:
        if extra_path not in sys.path:
            sys.path = [extra_path] + sys.path
