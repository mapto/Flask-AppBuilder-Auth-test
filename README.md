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

Where ldap_config.py can be replaced with your configuration. The current file assumes LDAP deployment in docker, as in the [KNOX Superset testing](https://github.com/mapto/knox_superset_testing) configuration. The [provided credentials](https://gitbox.apache.org/repos/asf?p=knox.git;a=blob;f=gateway-release/home/conf/users.ldif;h=986704dc40b9cee0a1fa4b3074aa4fb2ee5e11b0;hb=HEAD) can be read from the corresponding configuration file.

For tests with various authorisation paradigms (also reliant on LDAP credentials), try respectively:

### Login form

Start application with:

    python fab-getparam-test.py --config ldap_config.py --debug

then send request:

    curl 'http://localhost:8080/autologin/' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Connection: keep-alive' -H 'Cookie: session=.eJwdy9sKAiEQANB_mWdBbXW9_EqEDDqTkeSivkT07y29n_OBxINmhcjYJgnIc3Ba_UkviMB7CJvVKhtma0rRJlNx-4beaWt0wHIpznkDAlrP2Og8ZxRw4J1SfczVxxviFepaR5Tyj2qfK3rllYTb9wcUsSf5.XIps5w.pcPOgrJ1DDUhilDAjk-JGpBs_IA' -H 'Upgrade-Insecure-Requests: 1' --data 'csrf_token=ImY2OTkzNTEwYzRmZjU0ZGQxNGNlZDc2M2E4NzE1NDE5YWQyZDc3ODQi.XIps5w.KOE1XliSq2hmgcdsrH5s-ThTsfY&user.name=tom' -H 'Referer: http://localhost:8080/login/' -H 'Content-Type: application/x-www-form-urlencoded' 

### Basic authentiation

Start application:    
    
    python fab-ldap-test.py --config ldap_config.py --debug

Request:

    curl -ivk 'http://localhost:8080/autologin/' -H 'User-Agent: Mozil; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Connection: keep-alive' -H 'Cookie: session=.eJwdjkEKgzAURK8S_lqq1mg0N-iu-yLyMT8mNCSShBaR3r1pVwPDvJk5YdEOk6EE8nECy0XgjdFbv0EFN_9CZxVzYbP-wu6OMBHL8WC4YXFg_sxVqYiUDEiNLlEFa4p6yeFJHiToYZq6vm1WrnXPlWr5SkoMHY6i7Xk7oboqIUZexlxY0VFhCljBjhstxqYc4vE7ZXLeZV3_QyakLMdmbOpy4Atblj6B.XIpqIw.HxvKKorjH51LoFeWWoLQBuUmy2g' -H 'Upgrade-Insecure-Requests: 1' -H 'Authorization: Basic dG9tOnRvbS1wYXNzd29yZA==' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache'


### Hadoop-JWT

Start application:

    python fab-jwt-test.py --config jwt_config.py --debug
