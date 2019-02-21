#!/usr/bin/env python3
"""FlaskAppBuilder-LDAP Test

Usage:
	fab-ldap-test --help
	fab-ldap-test [options]

Examples:
	fab-ldap-test --port=8080
	fab-ldap-test --config=custom_config.py -d
	fab-ldap-test --config=/opt/custom_config.py -p8080
	fab-ldap-test -c C:\\tmp\\custom_config.py -p 8080

Options:
 -h --help             Show this screen.
 -p --port=<port>      Port used by this test server [default: 8080].
 -d --debug            Start in debug mode.
 -c --config=<config>  LDAP config file, with variables as in https://flask-appbuilder.readthedocs.io/en/latest/security.html#authentication-ldap 

For further documentation see README file.

"""
from importlib import import_module
import sys, os

from docopt import docopt

args = docopt(__doc__)

debug = args['--debug']

from webapp import create_app

config_name = os.path.abspath(args['--config'] if args['--config'] else 'db_config.py')
if debug: print("Loading config from: %s"%config_name)
local_app = create_app(config_name)

from webapp import app
app = local_app

app.run(host='0.0.0.0', port=args['--port'], debug=False)  # pyinstaller one file packaging confuses flask autorestart when debugging


