from flask import Flask

from config import Config
from .extensions import db
from .customers import customers_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.app = app
    db.init_app(app)

    # Register blueprints here
    app.register_blueprint(customers_bp)

    return app