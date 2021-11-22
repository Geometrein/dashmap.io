# Dash and Plotly
from dash import html
import dash_bootstrap_components as dbc

from .individual import init_census_individual_accordion
from .household import init_census_household_accordion


def init_tab_census() -> object:
    """
    Initialize the census tab.
    Args: None

    Returns: 
        census_tab_content (object): dash dbc.Card() that contains all relevant accordions
    """
    # Get accordion contents
    census_individuals_accordion = init_census_individual_accordion()
    census_households_accordion = init_census_household_accordion()

    census_tab_content = dbc.Card(
        dbc.CardBody(
            [   
                html.H2("Census", style={'marginBottom': 10, 'marginTop':1}),
                html.P(
                        """
                        A census is a complete enumeration of population and its vital characteristics.
                        Censuses are created by systematic recording and aggregation of data about the members of a given population.
                        The purpose populations census is to understand the basic structure of the society and identify emerging patterns and trends.
                        """,
                        className="card-text"
                    ),
                html.H4("Individuals", style={'marginBottom': 10, 'marginTop': 20}),
                html.P(
                        """
                        In this section information is aggregated on a level of an individuals. 
                        Members of the population are grouped by their Age, Gender, Education level, Emploment status and income levels.
                        """
                ),
                html.Div(census_individuals_accordion),
                html.H4("Households", style={'marginBottom': 10, 'marginTop': 20}),
                html.P(
                        """
                        In this section information is aggregated on a level of Households.
                        Members of the population are grouped by their Households Size, household Structure,
                        Household income and Household Dwelling type.
                        """
                ),
                html.Div(census_households_accordion),
                html.Hr(),
                html.P(
                    """
                    Data Source: PAAVO, Statistics Finland, 
                    Creative Commons Attribution 4.0 International
                    """),
            ]
        ), className="mt-3",
    )

    return census_tab_content