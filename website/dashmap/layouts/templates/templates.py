# Dash and Plotly
from dash import html
import dash_bootstrap_components as dbc


def init_accordion_element(title: str, graph_id: str, tab_n: int, group_n: int) -> object:
    """
    This function defines the template for the accordion cards.
    Args:
        title (str): Title of the card
        graph_id (str): id of the collapse
        tab_n (int): Number of the card
        group_n (int): Number of the group

    Returns: 
        accordion (object)
    """
    accordion = dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        title,
                        color="#303030",
                        id=f"tab-{tab_n}-group-{group_n}-toggle",
                        n_clicks=0,
                    )
                )
            ),
            
            dbc.Collapse(
                dbc.CardBody(
                    id=graph_id,
                    children=[]
                ),
                id=f"tab-{tab_n}-collapse-{group_n}",
                is_open=False,
            ),
        ], color="#1E1E1E"
    )
    return accordion


def assemble_accordion(accordions: list) -> object:
    """
    Assembles list of elements into a single html.Div object
    Args: None

    Returns: 
        census_ind_accordion (object)
    """
    accordions_div = html.Div(
        accordions,
        className="accordion"
    )
    
    return accordions_div
