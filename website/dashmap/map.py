# Dash and Plotly
from dash import Dash

# Main layouts for the dashboards
from .map_layout import init_layout

# Dash Callbacks
from .map_callbacks import init_callbacks


def edit_index_string(app) -> object:
    """
    The function edits the default dash index string and adds Google analytics.
    ---
    Args: 
        app (object): Dash app

    Returns:
        app (object): Dash app with modified index string
    """
    app.index_string = """<!DOCTYPE html>
    <html>
        <head>
            <!-- Global site tag (gtag.js) - Google Analytics -->
            <script async src="https://www.googletagmanager.com/gtag/js?id=G-18M1PG12L9"></script>
            <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());

            gtag('config', 'G-18M1PG12L9');
            </script>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
        </head>
        <body>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>"""

    return app


def init_dashboard(server):
    """
    Initialize the dashboard.
    ---
    Args:
        server: the main Flask app

    Returns: ༼ つ ◕_◕ ༽つ 
    """
    # Initialize the Dash app
    dash_app = Dash(
        __name__,
        title="Dashmap",
        server=server,
        url_base_pathname='/helsinki/'
    )

    dash_app = edit_index_string(dash_app)

    dash_app.layout = init_layout()

    init_callbacks(dash_app)

    return dash_app.server
