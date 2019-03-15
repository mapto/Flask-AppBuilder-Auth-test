import logging

from flask import Flask
from flask_appbuilder import SQLA, AppBuilder

from .lazyinit import app, db, appbuilder

"""
 Logging configuration
"""

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

def create_app(config_name=None, indexview=None, security_manager_class=None):
    global app, db, appbuilder

    app = Flask(__name__)
    app.config.from_object('config')
    if config_name:
        app.config.from_pyfile(config_name)
    db = SQLA(app)
    appbuilder = AppBuilder(app, db.session, indexview=indexview, security_manager_class=security_manager_class)

    return app

"""
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""    
