import pytest
from api import create_app, db
from config import TestConfig

@pytest.fixture()
def app():

    # Enter setup code here
    app = create_app(config_class=TestConfig)
    with app.app_context():

        # reset the database
        db.drop_all()
        db.create_all()

    # Run the tests
    yield app

    # Enter tear down code here

@pytest.fixture()
def client(app):
    return app.test_client()