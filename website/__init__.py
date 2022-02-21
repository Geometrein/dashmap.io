"""
Initializes the main flask app.
"""
import os

import flask
from flask import Flask, render_template
from website.views import views
from website.dashmap.map import init_dashboard


def create_app() -> flask.Flask:
    """
    Create the main Flask app.
    ---
    Args: None
    Returns: Flask object
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24).hex()

    # Register App Blueprints
    app.register_blueprint(views, url_prefix='/')

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html', e=error), 404

    # Initiate the Dash app
    app = init_dashboard(app)

    return app
