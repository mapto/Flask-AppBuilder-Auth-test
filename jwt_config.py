SQLALCHEMY_TRACK_MODIFICATIONS = False

from flask_appbuilder.security.manager import AUTH_LDAP

AUTH_TYPE = AUTH_LDAP

# Will allow user self registration
AUTH_USER_REGISTRATION = True

# The default user self registration role
AUTH_USER_REGISTRATION_ROLE = "Admin"

# When using LDAP Auth, setup the ldap server
#AUTH_LDAP_SERVER = "ldap://ldap.example.com"
AUTH_LDAP_SERVER = "ldap://172.17.0.1"
AUTH_LDAP_USE_TLS = False
AUTH_LDAP_SEARCH = "ou=people,dc=hadoop,dc=apache,dc=org"
AUTH_LDAP_BIND_USER = "uid=admin,ou=people,dc=hadoop,dc=apache,dc=org"
AUTH_LDAP_BIND_PASSWORD = "admin-password"

from crypto import open_jks
jks_file = "/home/mapto/knox/knox_superset_testing/keystores/gateway.jks"
master_secret = "knox"

SECRET_KEY = open_jks(jks_file, master_secret)
