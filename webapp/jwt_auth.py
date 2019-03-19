"""Used for before_request"""

from flask import g, redirect, request, flash, session
from flask_login import login_user

from . import appbuilder

import logging
log = logging.getLogger(__name__)

def _get_jwt_username(token):
    import jwt
    from crypto import open_jks
    jks_file = "/home/mapto/knox/knox_superset_testing/keystores/gateway.jks"
    master_secret = "knox"

    SECRET_KEY = open_jks(jks_file, master_secret)
    # from config import SECRET_KEY # use jks.

    log.info("Secret is %s"%(SECRET_KEY))
    contents = jwt.decode(token, SECRET_KEY)
    username = contents['sub']
    log.info("Username %s"%(username))
    return username

def _get_jwt_token(cookie_header):
    jwt_key = "hadoop-jwt="

    for c in cookie_header.split(";"):
        cookie = c.strip()
        if cookie.startswith(jwt_key):
            jwt_token = cookie.strip()[len(jwt_key):]
            return jwt_token
    return None

def parse_jwt():
    from flask import g, request
    from flask_login import login_user

    if g.user is not None and g.user.is_authenticated:
        log.info("Already authenticated: %s"%g.user)
        return None

    log.info("Cookies: %s"%request.headers["Cookie"])
    jwt_token = _get_jwt_token(request.headers["Cookie"])
    log.info("Token: %s"%jwt_token)
    if not jwt_token:
        log.info("Failed parsing token")
        return "Failed"
    username = _get_jwt_username(jwt_token)
    log.info("Username %s"%username)
    user = appbuilder.sm.find_user(username)
    if not user:
        log.info("Authentication failed: %s"%user)
        return "Failed"
    login_user(user, remember=True)
    return None
