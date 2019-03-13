from flask import g, redirect, render_template
from flask_appbuilder import IndexView, expose
# from flask_appbuilder import ModelView
from . import appbuilder

"""
    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(MyModelView, "My View", icon="fa-folder-open-o", category="My Category", category_icon='fa-envelope')
"""
class LoginIndexView(IndexView):
    @expose('/')
    @expose('/<path:path>')
    def index(self):
        if g.user.is_anonymous:
            return redirect("/login")
        return IndexView.index(self)
