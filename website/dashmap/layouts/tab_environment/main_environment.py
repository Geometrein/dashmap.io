# Dash and Plotly
from dash import html
import dash_bootstrap_components as dbc

from .environment import init_environment_accordion


def init_tab_environment() -> object:
    """
    Initialize the environment tab.
    Args: None

    Returns: 
        environment_tab_content (object): dash dbc.Card() that contains all relevant accordions
    """
    environment_accordion = init_environment_accordion()

    environment_tab_content = dbc.Card(
        dbc.CardBody(
            [   
                html.H2("Environment", style={'marginBottom': 10, 'marginTop': 1}),
                html.P("""
                The  environment refers to the environmental conditions created as byproduct
                of man-made and natural processes. It includes metrics like pollution, noise, 
                wind patterns and radiation levels.
                """,
                       className="card-text"),
                html.Div(environment_accordion),
            ]
        ),
        className="mt-3",
    )
    return environment_tab_content
