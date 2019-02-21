# Flask-AppBuilder LDAP configuration test

A simple tool that allows login via LDAP. This is used to debug an installation of [Apache Superset](https://superset.incubator.apache.org), allowing for testing in a quasi-production environment.

The tool is prepackaged in a binary and takes the [LDAP properties](https://flask-appbuilder.readthedocs.io/en/latest/security.html#authentication-ldap) from an external file via the the `--config` option. If the option is not specified defaults to an `admin`:`admin` user.

For usage options see documentation in [fab-ldap-test.py](https://github.com/mapto/Flask-AppBuilder-LDAP-test/blob/master/fab-ldap-test.py) or use the `--help` option

## Dependencies

Requires [python3](https://www.python.org/downloads/). To install further prerequisites, use:

    pip3 install flask-appbuilder python-ldap pyinstaller docopt
