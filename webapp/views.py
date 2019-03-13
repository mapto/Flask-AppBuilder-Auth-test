import logging

from flask import g, redirect, render_template, request
from flask_appbuilder import IndexView, expose
# from flask_appbuilder import ModelView
from . import appbuilder

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

"""
    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(MyModelView, "My View", icon="fa-folder-open-o", category="My Category", category_icon='fa-envelope')
"""
class LoginIndexView(IndexView):
    @expose('/')
    # @expose('/<path:path>')
    def index(self, path=""):
        log.info("Path request is "%path)
        log.info("User is anonymous: "%g.user.is_anonymous)
        if g.user.is_anonymous:
            return redirect("/login")
            
        return IndexView.index(self)
