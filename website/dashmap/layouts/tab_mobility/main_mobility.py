# Dash and Plotly
from dash import html
import dash_bootstrap_components as dbc

from .mobility import init_mobility_accordion


def init_tab_mobility() -> object:
    """
    Initialize the mobility tab.
    Args: None

    Returns: 
        mobility_tab_content (object): dash dbc.Card() that contains all relevant accordions
    """
    mobility_accordion = init_mobility_accordion()
    
    mobility_tab_content = dbc.Card(
        dbc.CardBody(
            [
                html.H2("Mobility", style={'marginBottom': 10, 'marginTop': 1}),
                html.P(
                    """
                    Geographic mobility is the measure of how populations and goods move over time.
                    Population mobility has a large impact on many sociological factors in a society and has implications ranging
                    from impacts on local economic growth to housing markets and demand for regional services.
                    """,
                    className="card-text"
                ),
                html.Div(mobility_accordion),
            ]
        ),
        className="mt-3",
    )
    
    return mobility_tab_content
