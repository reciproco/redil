# -*- coding: utf-8 -*-
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os
import unittest
import coverage

from app import db, create_app

app = create_app()
app.app_context().push()
app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """Runs the unit tests without coverage."""
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    cov = coverage.coverage(
        branch=True,
        include='app/*'
    )
    cov.start()
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print('Coverage Summary:')
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'htmlcov')
    cov.html_report(directory=covdir)
    cov.erase()

if __name__ == '__main__':
    manager.run()
