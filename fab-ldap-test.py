#!/usr/bin/env python3
"""FlaskAppBuilder-LDAP Test

Usage:
	fab-ldap-test --help
	fab-ldap-test [options]

Examples:
	fab-ldap-test --port=8080
	fab-ldap-test --type=DB
	fab-ldap-test --port=8080 --type=DB

Options:
 -h --help         Show this screen.
 -p --port=<port>  Server port [default: 8080].
 -d --debug        Start in debug mode.
 -t --type=<type>  Authentication type [default: DB].
"""
from docopt import docopt
from app import app

from flask_appbuilder.security.manager import AUTH_DB, AUTH_LDAP
from config import AUTH_TYPE

auth_types = {"DB": AUTH_DB, "LDAP": AUTH_LDAP}

args = docopt(__doc__)
if args['--type']:
	AUTH_TYPE = auth_types[args['--type']]
app.run(host='0.0.0.0', port=args['--port'], debug=args['--debug'])

