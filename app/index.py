from flask import g, redirect
from flask_appbuilder import IndexView, expose

class LoginIndexView(IndexView):
    @expose('/')
    def index(self):
        if g.user.is_anonymous:
            return redirect("/login")
        return IndexView.index(self)

