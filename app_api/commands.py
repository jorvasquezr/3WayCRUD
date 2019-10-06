from flask.cli import AppGroup
from .modelsSQL import db

apps = AppGroup('apps')

@apps.command('create-tables')
def createTables():
    db.create_all()

def init_app(app):
    app.cli.add_command(apps)