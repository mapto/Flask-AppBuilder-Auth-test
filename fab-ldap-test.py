#!/usr/bin/env python3
"""FlaskAppBuilder-LDAP Test

Usage:
	fab-ldap-test --help
	fab-ldap-test [options]

Examples:
	fab-ldap-test --port=8080
	fab-ldap-test --config=custom_config.py -d

Options:
 -h --help             Show this screen.
 -p --port=<port>      Port used by this test server [default: 8080].
 -d --debug            Start in debug mode.
 -c --config=<config>  LDAP config file, with variables as in https://flask-appbuilder.readthedocs.io/en/latest/security.html#authentication-ldap 

For further documentation see README file.

"""
from importlib import import_module

from docopt import docopt
from app import app

from flask_appbuilder.security.manager import AUTH_DB, AUTH_LDAP
import config

args = docopt(__doc__)

AUTH_TYPE = AUTH_LDAP if args['--config'] else AUTH_DB	

if args['--config']:
	custom_config = import_module(args['--config'].split('.')[0])  # Get rid of file extension. Providing modules as filename is easier with autocomplete
	vals = [v for v in dir(custom_config) if v.startswith("AUTH_LDAP_")]
	for v in vals:
		setattr(config, v, getattr(custom_config, v))

app.run(host='0.0.0.0', port=args['--port'], debug=args['--debug'])

