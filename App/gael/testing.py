import sys

def add_appsever_import_paths():
    from dev_appserver import EXTRA_PATHS
    for extra_path in EXTRA_PATHS:
		if extra_path not in sys.path:
			sys.path = [extra_path] + sys.path 

def initialize_service_apis():
    from google.appengine.tools import dev_appserver

    from google.appengine.tools.dev_appserver_main import ParseArguments
    args, option_dict = ParseArguments(sys.argv) # Otherwise the option_dict isn't populated.
    dev_appserver.SetupStubs('local', **option_dict)
	