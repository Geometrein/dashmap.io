# Dash and Plotly
from dash import html
import dash_bootstrap_components as dbc

from .services import init_services_accordion

def init_tab_services() -> object:
    """
    Initialize the services tab.
    Args: None

    Returns: 
        (object): dash dbc.Card() that contains all relevant accordions
    """
    service_accordion = init_services_accordion()

    services_tab_content = dbc.Card(
        dbc.CardBody(
            [
                html.H2("Services", style={'marginBottom': 10, 'marginTop':1}),
                html.P(
                    """
                    A service is a transaction in which no physical goods are transferred from the seller to the buyer.
                    Services may be defined as acts or performances whereby the service provider provides value to the customer
                    using resources, skill, ingenuity or experience.
                    """
                ),
                html.Div(service_accordion),
                html.Hr(),
                html.P(
                    """
                    Data Source: PAAVO, Statistics Finland, 
                    Creative Commons Attribution 4.0 International
                    """),
            ]
        ),
        className="mt-3",
    )
    return services_tab_content