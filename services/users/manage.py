# services/users/manage.py
import sys
import unittest
import coverage

from flask.cli import FlaskGroup

# from project import app, db  # new
from project import create_app, db  # new
from project.api.models import User  # new

COV = coverage.coverage(
    branch=True, include="project/*", omit=["project/tests/*", "project/config.py",]
)
COV.start()

# cli = FlaskGroup(app)
app = create_app()  # new
cli = FlaskGroup(create_app=create_app)

# new


@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


# new


@cli.command()
def test():
    """Runs the tests withot code coverage."""
    tests = unittest.TestLoader().discover("project/tests", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)


@cli.command("seed_db")
def seed_db():
    """Seeds the database."""
    db.session.add(User(username="fredy.huanca", email="abelthf@gmail.com"))
    db.session.add(User(username="abel.huanca", email="abel.huanca@upeu.edu.pe"))
    db.session.commit()


@cli.command()
def cov():
    """Run the unit test with coverage."""
    tests = unittest.TestLoader().discover("project/tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print("Coverage Summary: ")
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    sys.exit(result)


if __name__ == "__main__":
    cli()
