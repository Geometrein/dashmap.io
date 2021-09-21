import os
from flask import Flask

# Create the Flask app
def create_app():
    """
    Create the main Flask app.
    ---
    Args: None

    Returns: Flask object
    """
    # Initiate the Flask object
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24).hex()

    # Register App Blueprints
    from .views import views
    app.register_blueprint(views, url_prefix='/')

    # Initiate the Dash app
    from .dashmap.map import init_dashboard
    app = init_dashboard(app)

    return app



