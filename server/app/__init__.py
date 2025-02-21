from flask import Flask
from app.config import Config
from app.routes import routes
from app.db import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(routes)

    return app
