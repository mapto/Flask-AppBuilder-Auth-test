# Flask-AppBuilder Authentication configuration test

A simple tool that allows login via LDAP. This is used to debug an installation of [Apache Superset](https://superset.incubator.apache.org), allowing for testing in a quasi-production environment.

The tool is prepackaged in a binary and takes the [LDAP properties](https://flask-appbuilder.readthedocs.io/en/latest/security.html#authentication-ldap) from an external file via the the `--config` option. If the option is not specified defaults to an `admin`:`admin` user.

For usage options see documentation in [fab-ldap-test.py](https://github.com/mapto/Flask-AppBuilder-LDAP-test/blob/master/fab-ldap-test.py) or use the `--help` option

## Dependencies

Requires [python3](https://www.python.org/downloads/). To install further prerequisites, use:

    pip3 install -r requirements.txt

## Usage

For LDAP authentication call e.g.

    python fab-ldap-test.py --config ldap_config.py --debug

Where ldap_config.py can be replaced with your configuration. The current file assumes LDAP deployment in docker, as in the [KNOX Superset testing](https://github.com/mapto/knox_superset_testing) configuration.

For tests with various authorisation paradigms, try respectively:

    python fab-getparam-test.py --config ldap_config.py --debug
    python fab-ldap-test.py --config ldap_config.py --debug

Notice that this configurations also rely on the user being present in LDAP.
