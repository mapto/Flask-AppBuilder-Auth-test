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
from app import app

from flask_appbuilder.security.manager import AUTH_DB, AUTH_LDAP
import config

args = docopt(__doc__)

debug = args['--debug']

AUTH_TYPE = AUTH_LDAP if args['--config'] else AUTH_DB	

if args['--config']:
	if debug: print("Loading LDAP config: %s"%args['--config'])
	(path, filename) = os.path.split(args['--config'])
	path = os.path.abspath(path if path else os.path.curdir)
	sys.path.insert(0, path)
	if debug: print("Searching in path: %s"%path)
	(config_name, ext) = os.path.splitext(filename)
	custom_config = import_module(config_name)  # Get rid of file extension. Providing modules as filename is easier with autocomplete
	vals = [v for v in dir(custom_config) if v.startswith("AUTH_LDAP_")]
	for v in vals:
		if debug: print("Setting %s\t= %s"%(v, getattr(custom_config, v)))
		setattr(config, v, getattr(custom_config, v))
else:
	if debug: print("Serving without LDAP with user admin:admin")

app.run(host='0.0.0.0', port=args['--port'], debug=False)  # pyinstaller one file packaging confuses flask autorestart when debugging


