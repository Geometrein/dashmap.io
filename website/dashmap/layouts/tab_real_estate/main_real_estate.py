# Dash and Plotly
from dash import html
import dash_bootstrap_components as dbc

from .estate import init_real_estate_accordion

def init_tab_real_estate() -> object:
    """
    Initialize the real estate tab.
    Args: 
        real_estate_accordion (object): real estate accordion contents

    Returns: 
        real_estate_tab_content (object): dash dbc.Card() that contains all relevant accordions
    """
    real_estate_accordion = init_real_estate_accordion()

    real_estate_tab_content = dbc.Card(
        dbc.CardBody(
            [
                html.H2("Real Estate", style={'marginBottom': 10, 'marginTop':1}),
                html.P(
                    """
                    Real estate is a type of real property consisting of land along with any permanent improvements attached to the land.
                    The included resources can be man made or natural. They can include water, trees, crops minerals and built structures. 
                    Often the value of real estate is one of the key indicators of an economy’s health.
                    """,
                    className="card-text"
                ),
                html.H3("Residential", style={'marginBottom': 10, 'marginTop': 20}),
                html.P(
                    """
                    Residential real estate is broadly defined as real property used for residential purposes. 
                    The most common examples of residential property are blocks of flats and single-family homes.
                    """,
                    className="card-text"
                ),
                html.Div(real_estate_accordion),
                html.Hr(),
            ]
        ),
        className="mt-3",
    )
    
    return real_estate_tab_content