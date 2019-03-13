import base64
import logging

import jwt

from flask import g, redirect, request, flash
from flask_login import login_user
from flask_appbuilder import expose
from flask_appbuilder._compat import as_unicode
from flask_appbuilder.security.views import AuthView

from superset.security import SupersetSecurityManager

log = logging.getLogger(__name__)


class NoAuthView(AuthView):
    @expose('/login/', methods=['GET', 'POST'])
    def login(self):
        if g.user is not None and g.user.is_authenticated:
            return redirect(self.appbuilder.get_url_for_index)

        username = request.args.get("user.name")
        log.info("Username %s"%username)
        user = self.appbuilder.sm.find_user(username)
        if not user:
            flash(as_unicode(self.invalid_login_message), 'warning')
            return redirect(self.appbuilder.get_url_for_login)
        login_user(user, remember=True)
        return redirect(self.appbuilder.get_url_for_index)

class NoSecurityManager(SupersetSecurityManager):
    # authdbview = AuthJWTView
    authdbview = NoAuthView


class BasicAuthView(AuthView):
    def _get_basic_credentials(self, auth_header):
        if auth_header[:6] != "Basic ":
            return None
        credentials = str(base64.b64decode(auth_header[6:])).split(":")
        log.info("Credentials %s:%s"%(credentials[0],credentials[1]))
        return credentials[0], credentials[1]

    @expose('/login/', methods=['GET', 'POST'])
    def login(self):
        if g.user is not None and g.user.is_authenticated:
            return redirect(self.appbuilder.get_url_for_index)

        u,p = self._get_basic_credentials(request.headers["Authorization"])
        user = self.appbuilder.sm.auth_user_ldap(u, p)
        if not user:
            flash(as_unicode(self.invalid_login_message), 'warning')
            return redirect(self.appbuilder.get_url_for_login)
        login_user(user, remember=True)
        return redirect(self.appbuilder.get_url_for_index)

class BasicAuthSecurityManager(SupersetSecurityManager):
    # authdbview = AuthJWTView
    authdbview = BasicAuthView


class AuthJWTView(AuthView):
    def _get_jwt_username(self, token):
        from config import SECRET_KEY # use jks.
        print(SECRET_KEY)        
        username = jwt.decode(token, SECRET_KEY)
        log.info("Username %s"%(username))
        return username

    @expose('/login/', methods=['GET', 'POST'])
    def login(self):
        if g.user is not None and g.user.is_authenticated:
            return redirect(self.appbuilder.get_url_for_index)

        print(request.headers["Cookie"])
        jwt_key = " hadoop-jwt="
        jwt_token = [t[len(jwt_key):] for c in request.headers["Cookie"].split(";") if c.startswith(jwt_key)][0]
        print(jwt_token)
        username = self._get_jwt_username(jwt_token)
        print(username)
        user = self.appbuilder.sm.find_user(username)
        if not user:
            flash(as_unicode(self.invalid_login_message), 'warning')
            return redirect(self.appbuilder.get_url_for_login)
        login_user(user, remember=True)
        return redirect(self.appbuilder.get_url_for_index)

class JwtSecurityManager(SupersetSecurityManager):
    authdbview = AuthJWTView
