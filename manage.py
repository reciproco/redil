# -*- coding: utf-8 -*-
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

from app import db, create_app

app = create_app()
app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
