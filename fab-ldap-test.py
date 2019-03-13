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
import os
import logging

from docopt import docopt

args = docopt(__doc__)

debug = args['--debug']
logging.getLogger().setLevel(logging.DEBUG if debug else logging.INFO)

from webapp import create_app
from webapp.views import LoginIndexView

config_name = os.path.abspath(args['--config']) if args['--config'] else None
if debug: print("Loading config from: %s"%config_name)
local_app = create_app(config_name=config_name, indexview=LoginIndexView)

from webapp import app
app = local_app

app.run(host='0.0.0.0', port=args['--port'], debug=False)  # pyinstaller one file packaging confuses flask autorestart when debugging


