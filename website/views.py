from flask import Blueprint, render_template

views = Blueprint('views', __name__)

def base():
    """
    Load the main html template
    Args: None

    Returns: 
        base.html (str): base html template 
    """
    return render_template("base.html")

@views.route('/')
@views.route('/home')
def home():
    """
    Loads the home html template
    Args: None

    Returns: 
        home.html (str): home html template
    """
    return render_template("home.html")

@views.route('/support')
def about():
    """
    Loads the about html template
    Args: None

    Returns: 
        about.html (str): about html template
    """
    return render_template("support.html")
