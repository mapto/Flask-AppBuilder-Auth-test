import base64
import logging

import jwt

from flask import g, redirect, request, flash, session
from flask_login import login_user
from flask_appbuilder import expose
from flask_appbuilder.forms import DynamicForm
from flask_appbuilder.security.forms import LoginForm_db
from flask_appbuilder._compat import as_unicode
from flask_appbuilder.security.views import AuthView

from flask_appbuilder.security.sqla.manager import SecurityManager

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class NoAuthView(AuthLDAPView):
    @expose('/autologin/', methods=['GET', 'POST'])
    def login(self):
        if g.user is not None and g.user.is_authenticated:
            log.info("User is already authenticated: %s"%(g.user))
            return redirect(self.appbuilder.get_url_for_index)

        username = request.args.get("user.name")
        log.info("Username %s"%username)
        user = self.appbuilder.sm.find_user(username)
        if not user:
            flash(as_unicode(self.invalid_login_message), 'warning')
            return redirect(self.appbuilder.get_url_for_login)
        login_user(user, remember=True)
        return redirect(self.appbuilder.get_url_for_index)

class NoSecurityManager(SecurityManager):
    # authdbview = AuthJWTView
    authldapview = NoAuthView

"""
class BasicAuthView(AuthView):
    # def __init__(self):
    #     super(AuthOIDView, self).__init__()

    @expose('/autologin/', methods=['GET', 'POST'])
    def login(self, flag=True):
        @self.appbuilder.sm.oid.loginhandler
        def login_handler(self):
            if g.user is not None and g.user.is_authenticated:
                return redirect(self.appbuilder.get_url_for_index)

            auth_header = request.headers.get("Authorization", None)
            if not auth_header:
                session['remember_me'] = True
                return self.appbuilder.sm.oid.try_login(form.openid.data, ask_for=self.oid_ask_for,
                                                        ask_for_optional=self.oid_ask_for_optional)
            return self.render_template(self.login_template,
                                   title=self.title,
                                   form=form,
                                   providers=self.appbuilder.sm.openid_providers,
                                   appbuilder=self.appbuilder
            )

        @self.appbuilder.sm.oid.after_login
        def after_login(resp):
            if resp.email is None or resp.email == "":
                flash(as_unicode(self.invalid_login_message), 'warning')
                return redirect('login')
            user = self.appbuilder.sm.auth_user_oid(resp.email)
            if user is None:
                flash(as_unicode(self.invalid_login_message), 'warning')
                return redirect('login')
            remember_me = False
            if 'remember_me' in session:
                remember_me = session['remember_me']
                session.pop('remember_me', None)

            login_user(user, remember=remember_me)
            return redirect(self.appbuilder.get_url_for_index)

        return login_handler(self)

"""
class BasicAuthView(AuthLDAPView):
    # login_template = 'autologin.html'
    # title = "Autologin"

    def _get_basic_credentials(self, auth_header):
        log.info("Authorization header: %s"%auth_header)
        if not auth_header or auth_header[:6] != "Basic ":
            log.info("Unexpected header: %s"%(auth_header))
            return None
        credentials = base64.b64decode(auth_header[6:]).decode().split(":")
        log.info("Credentials %s:%s"%(credentials[0],credentials[1]))
        return credentials[0], credentials[1]

    @expose('/autologin', methods=['GET', 'POST'])
    @expose('/autologin/', methods=['GET', 'POST'])
    def autologin(self):
        # import pdb; pdb.set_trace()
        if g.user is not None and g.user.is_authenticated:
            log.info("User is already authenticated: %s"%(g.user))
            return redirect(self.appbuilder.get_url_for_index)
        form = LoginForm_db()

        auth_header = request.headers.get("Authorization", None)
        log.info("Authorization header is %s"%(auth_header))
        if not auth_header:
            return self.render_template(self.login_template,
                               title=self.title,
                               form=form,
                               appbuilder=self.appbuilder)
        else:
            u,p = self._get_basic_credentials(auth_header)
            form.username.data = u
            form.password.data = p
        if not form.validate_on_submit():
            flash(as_unicode(self.invalid_login_message), 'warning')
            return redirect(self.appbuilder.get_url_for_login)            
        user = self.appbuilder.sm.auth_user_ldap(u, p)
        log.info("User is %s"%user)
        if not user:
            flash(as_unicode(self.invalid_login_message), 'warning')
            return redirect(self.appbuilder.get_url_for_login)
        remember_me = False
        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)

        self.appbuilder.sm.update_user_auth_stat(user, success=True)
        login_user(user, remember=True)        

        return redirect(self.appbuilder.get_url_for_index)

class BasicAuthSecurityManager(SecurityManager):
    # authdbview = AuthJWTView
    authldapview = BasicAuthView


class AuthJWTView(AuthLDAPView):
    def _get_jwt_username(self, token):
        from config import SECRET_KEY # use jks.
        log.info("Secret is %s"%(SECRET_KEY))
        contents = jwt.decode(token, SECRET_KEY)
        username = contents['sub']
        log.info("Username %s"%(username))
        return username

    @expose('/login/', methods=['GET', 'POST'])
    def login(self):
        if g.user is not None and g.user.is_authenticated:
            log.info("User is already authenticated: %s"%g.user)
            return redirect(self.appbuilder.get_url_for_index)

        log.info("Cookies: %s"%request.headers["Cookie"])
        jwt_key = "hadoop-jwt="
        jwt_token = [t[len(jwt_key):] for c in request.headers["Cookie"].split(";") if c.strip().startswith(jwt_key)][0]
        log.info("Token: %s"%jwt_token)
        username = self._get_jwt_username(jwt_token)
        log.info("Username %s"%username)
        user = self.appbuilder.sm.find_user(username)
        if not user:
            flash(as_unicode(self.invalid_login_message), 'warning')
            return redirect(self.appbuilder.get_url_for_login)
        login_user(user, remember=True)
        return redirect(self.appbuilder.get_url_for_index)

class JwtSecurityManager(SecurityManager):
    authldapview = AuthJWTView

