"""
This module registers flask app views.
"""
from flask import Blueprint, render_template

views = Blueprint('views', __name__)


def base() -> str:
    """
    Loads the main html template.
    ---
    Args: None

    Returns:
        base.html: base html template.
    """
    return render_template("base.html")


@views.route('/', methods=['GET'])
@views.route('/home', methods=['GET'])
def home() -> str:
    """
    Loads the home html template.
    ---
    Args: None

    Returns:
        home.html: home html template.
    """
    return render_template("home.html")


@views.route('/support', methods=['GET'])
def about() -> str:
    """
    Loads the about html template.
    ---
    Args: None

    Returns:
        support.html: support html template
    """
    return render_template("support.html")
