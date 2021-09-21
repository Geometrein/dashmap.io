# Dash and Plotly
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

# Plotly Graph Objects
from .map_graphs import *



def init_navbar():
    """
    Initialize the navbar inside te dash app.
    Args: None

    Returns: 
        navbar (object): dash bootstrap component NavbarSimple
    """
    navbar = dbc.NavbarSimple(
                children=[
                    dbc.NavItem(dbc.NavLink("Home", href="/", external_link=True)),
                    dbc.NavItem(dbc.NavLink("About", href="/about", external_link=True)),
                    dbc.Button(
                        "Help", 
                        id="help-open-centered",
                        color="link",
                        size="sm",
                        className="mr-1",
                        outline=True,
                    ),
                    dbc.Modal(
                        [
                            dbc.ModalHeader("🎊 Welcome to Dashmap! 🎊 "),
                            dbc.ModalBody(
                                children=[
                                    html.Img(
                                        src='/assets/help.gif', 
                                        style = {
                                            'display': 'block',
                                            'margin-left': 'auto',
                                            'margin-right': 'auto',
                                            'width': '100%'
                                        }
                                    ),
                                    html.P(
                                        """
                                        Use the map to filter the data by postal area.
                                        You can select a postal area by clicking on it on the map. Double click will select all postal areas.
                                        The data displayed on the map can be filtered too. Click on the legend of the map to show/Hide different layers.
                                        """
                                    )
                                ]
                            ),
                            dbc.ModalFooter(
                                dbc.Button(
                                    "Got it!",
                                    id="help-close-centered",
                                    className="ml-auto",
                                    n_clicks=0,
                                )
                            ),
                        ],
                        id="help-modal-centered",
                        size="lg",
                        centered=True,
                        is_open=False,
                    ), 
                ],
                brand="Dashmap",
                brand_href="/",
                color="#1a1c22",
                dark=True,
                fluid =True
    )

    return navbar

def init_census_individual_accordion():
    """
    Initialize the accordion for census tab.
    Args: None

    Returns: 
        census_individuals_accordion (object): dash html.Div that contains individual accordions
    """
    accordion_age = dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        "Age",
                        color="#303030",
                        id=f"tab-1-group-1-toggle",
                        n_clicks=0,
                        block=True,
                    )
                )
            ),
            dbc.Collapse(
                dbc.CardBody(
                    id='id_age_dist_hist',
                    children=[]
                ),
                id=f"tab-1-collapse-1",
                is_open=False,
            ),
        ], 
        color="#1E1E1E"
    )

    accordion_gender = dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        "Gender",
                        color="#303030",
                        id=f"tab-1-group-2-toggle",
                        n_clicks=0,
                        )
                    )
            ),
            dbc.Collapse(
                dbc.CardBody(
                    id='id_gender_pie_chart',
                    children=[]
                ),
                id=f"tab-1-collapse-2",
                is_open=False,
            ),
        ],
        color="#1E1E1E"
    )

    accordion_education = dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        "Education",
                        color="#303030",
                        id=f"tab-1-group-3-toggle",
                        n_clicks=0,
                    )
                )
            ),
            dbc.Collapse(
                dbc.CardBody(
                    id='id_education_pie_chart',
                    children=[]
                ),
                id=f"tab-1-collapse-3",
                is_open=False,
            ),
        ],
        color="#1E1E1E"
    )

    accordion_income = dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        "Income",
                        color="#303030",
                        id=f"tab-1-group-4-toggle",
                        n_clicks=0,
                    )
                )
            ),
            dbc.Collapse(
                dbc.CardBody(
                    id = 'id_income_pie_chart',
                    children=[]
                ),
                id=f"tab-1-collapse-4",
                is_open=False,
            ),
        ],
        color="#1E1E1E"
    )

    accordion_employment = dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        "Employment",
                        color="#303030",
                        id=f"tab-1-group-5-toggle",
                        n_clicks=0,
                    )
                )
            ),
            dbc.Collapse(
                dbc.CardBody(
                    id = 'id_employment_pie_chart',
                    children=[]
                ),
                id=f"tab-1-collapse-5",
                is_open=False,
            ),
        ], color="#1E1E1E"
    )


    census_individuals_accordion = html.Div(
        [
            accordion_age,
            accordion_gender,
            accordion_education,
            accordion_income,
            accordion_employment
        ],
        className="accordion"
    )
    return census_individuals_accordion

def init_census_household_accordion():
    """
    Initialize the second accordion for census tab.
    Args: None

    Returns: 
        census_households_accordion (object): dash html.Div that contains individual accordions
    """
    accord_household_size = dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        "Household Size",
                        color="#303030",
                        id=f"tab-1-2-group-1-toggle",
                        n_clicks=0,
                    )
                )
            ),
            dbc.Collapse(
                dbc.CardBody(
                    id='id_household_size',
                    children=[]
                ),
                id=f"tab-1-2-collapse-1",
                is_open=False,
            ),
        ],
        color="#1E1E1E"
    )

    accord_household_structure = dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        "Household Structure",
                        color="#303030",
                        id=f"tab-1-2-group-2-toggle",
                        n_clicks=0,
                        )
                    )
            ),
            dbc.Collapse(
                dbc.CardBody(
                    id='id_household_structure',
                    children=[]
                ),
                id=f"tab-1-2-collapse-2",
                is_open=False,
            ),
        ],
        color="#1E1E1E"
    )

    accord_household_income = dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        "Household Income",
                        color="#303030",
                        id=f"tab-1-2-group-3-toggle",
                        n_clicks=0,
                    )
                )
            ),
            dbc.Collapse(
                dbc.CardBody(id='id_household_income', children=[]
                ),
                id=f"tab-1-2-collapse-3",
                is_open=False,
            ),
        ],
        color="#1E1E1E"
    )

    accord_household_dwell= dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        "Household dwelling type",
                        color="#303030",
                        id=f"tab-1-2-group-4-toggle",
                        n_clicks=0,
                    )
                )
            ),
            dbc.Collapse(
                dbc.CardBody(
                    id = 'id_household_dwellings',
                    children=[]
                ),
                id=f"tab-1-2-collapse-4",
                is_open=False,
            ),
        ],
        color="#1E1E1E"
    )

    census_households_accordion = html.Div(
        [
            accord_household_size,
            accord_household_structure,
            accord_household_income,
            accord_household_dwell
        ],
        className="accordion"
    )

    return census_households_accordion

def init_real_estate_accordion():
    """
    Initialize the real estate accordion for real estate tab.
    Args: None

    Returns: 
        real_estate_accordion (object): dash html.Div that contains individual accordions
    """
    accord_re_owning = dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                        dbc.Button(
                            "Ownership",
                            color="#303030",
                            id=f"tab-2-group-2-toggle",
                            n_clicks=0,
                        )
                )
            ),
            dbc.Collapse(
                dbc.CardBody(
                    id='id_re_owning',
                    children=[]
                ),
                id=f"tab-2-collapse-2",
                is_open=False,
            ),
        ],
        color="#1E1E1E"
    )

    accord_re_renting = dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        "Rentals",
                        color="#303030",
                        id=f"tab-2-group-3-toggle",
                        n_clicks=0,
                    )
                )
            ),
            dbc.Collapse(
                dbc.CardBody(
                    id='id_re_renting',
                    children=[]
                ),
                id=f"tab-2-collapse-3",
                is_open=False,
            ),
        ],
        color="#1E1E1E"
    )

    accord_re_sauna = dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        "Sauna Index 🛁",
                        color="#303030",
                        id=f"tab-2-group-4-toggle",
                        n_clicks=0,
                    )
                )
            ),
            dbc.Collapse(
                dbc.CardBody(
                    id='id_re_sauna',
                    children=[]
                ),
                id=f"tab-2-collapse-4",
                is_open=False,
            ),
        ],
        color="#1E1E1E"
    )

    forecasts_card = dbc.Card(
        [
            dbc.CardImg(src="assets/nasa.png", top=True),
            dbc.CardBody(
                [
                    html.H4(
                        "Explore the future with us!",
                        className="card-title"
                    ),
                    html.P(
                        "Harness the full power of our cutting edge platform."
                        "make up the bulk of the card's content.",
                        className="card-text",
                    ),
                    dbc.Button(
                        "Join!",
                        color="primary"
                    ),
                ]
            ),
        ],
    )

    real_estate_accordion = html.Div(
        [
            accord_re_renting,
            accord_re_owning,
            accord_re_sauna
        ],
        className="accordion"
    )
    return real_estate_accordion

def init_services_accordion():
    """
    Initialize the services accordion for services tab.
    Args: None

    Returns: 
        services_accordion (object): dash html.Div that contains individual accordions
    """

    services_accordion = html.Div(
        [

        ],
        className="accordion"
    )
    return services_accordion
    
def init_mobility_accordion():
    """
    Initialize the mobility accordion for mobility tab.
    Args: None

    Returns: 
        mobility_accordion (object): dash html.Div that contains individual accordions
    """

    mobility_accordion = html.Div(
        [

        ],
        className="accordion"
    )
    return mobility_accordion

def tab_census(census_individuals_accordion, census_households_accordion):
    """
    Initialize the census tab.
    Args: 
        census_individuals_accordion (object): individual accordion
        census_households_accordion (object): household accordion

    Returns: 
        census_tab_content (object): dash dbc.Card() that contains all relevant accordions
    """
    census_tab_content = dbc.Card(
        dbc.CardBody(
            [   
                html.H2("Census", style={'marginBottom': 10, 'marginTop':1}),
                html.P(
                        """
                        A census is the procedure of systematically calculating, acquiring and recording information about the members of a given population.
                        """,
                        className="card-text"
                    ),
                html.H4("Individuals", style={'marginBottom': 10, 'marginTop': 20}),
                html.P(
                        """
                        A census is the procedure of systematically calculating, acquiring and recording information about the members of a given population.
                        """
                ),
                html.Div(census_individuals_accordion),
                html.H4("Households", style={'marginBottom': 10, 'marginTop': 20}),
                html.P(
                        """
                        A census is the procedure of systematically calculating, acquiring and recording information about the members of a given population.
                        """
                ),
                html.Div(census_households_accordion),
            ]
        ),
        className="mt-3",
    )
    return census_tab_content

def tab_real_estate(real_estate_accordion, real_estate_scatter):
    """
    Initialize the real estate tab.
    Args: 
        real_estate_accordion (object): real estate accordion contents

    Returns: 
        real_estate_tab_content (object): dash dbc.Card() that contains all relevant accordions
    """

    real_estate_tab_content = dbc.Card(
        dbc.CardBody(
            [
                html.H2("Real Estate", style={'marginBottom': 10, 'marginTop':1}),
                html.P(
                    """
                    Real estate is property consisting of land and the buildings on it, along with its natural resources such as crops, minerals or water.
                    It can be used for residential, commercial, or industrial purposes. 
                    Often the value of real estate is one of the key indicators of an economy’s health.
                    """,
                    className="card-text"
                ),
                html.H4("Residential", style={'marginBottom': 10, 'marginTop': 20}),
                html.P(
                    """
                    Real estate is property consisting of land and the buildings on it, along with its natural resources such as crops, minerals or water.
                    It can be used for residential, commercial, or industrial purposes. 
                    Often the value of real estate is one of the key indicators of an economy’s health.
                    """,
                    className="card-text"
                ),
                html.Div(real_estate_scatter),
                html.Div(real_estate_accordion),
            ]
        ),
        className="mt-3",
    )

    return real_estate_tab_content

def tab_mobility(mobility_accordion):
    """
    Initialize the mobility tab.
    Args: 
        mobility_accordion (object): mobility accordion contents

    Returns: 
        mobility_tab_content (object): dash dbc.Card() that contains all relevant accordions
    """
    mobility_tab_content = dbc.Card(
        dbc.CardBody(
            [
                html.H2("Mobility", style={'marginBottom': 10, 'marginTop':1}),
                html.P(
                    """
                    Geographic mobility is the measure of how populations and goods move over time.
                    Mobility is also a statistic that measures migration within
                    a population. Geographic mobility has a large impact on many sociological factors in a community and is a
                    current topic of academic research. Population mobility has implications ranging
                    from administrative changes in government and impacts on local economic growth to housing markets and demand for regional
                    services.
                    -Car accidents
                    -bike paths
                    -high flow of people
                    -advertizement
                    -points of interest 
                    """,
                    className="card-text"
                ),
                html.Div(mobility_accordion),
            ]
        ),
        className="mt-3",
    )
    return mobility_tab_content

def tab_services(service_accordion):
    """
    Initialize the services tab.
    Args: 
        service_accordion (object): service accordion contents

    Returns: 
        services_tab_content (object): dash dbc.Card() that contains all relevant accordions
    """
    services_tab_content = dbc.Card(
        dbc.CardBody(
            [
                html.H2("Services", style={'marginBottom': 10, 'marginTop':1}),
                html.P(
                    """
                    A service is a transaction in which no physical goods are transferred from the seller to the buyer.
                    The benefits of such a service are held to be demonstrated by the buyer's willingness to make the exchange.
                    Public services are those that society as a whole pays for.
                    Using resources, skill, ingenuity, and experience, service providers benefit service consumers.
                    Service is intangible in nature. Services may be defined as acts or performances whereby the service provider provides value to the customer.
                    """
                ),
                html.Div(),
            ]
        ),
        className="mt-3",
    )
    return services_tab_content

def tab_environment(environment_accordion):
    """
    Initialize the environment tab.
    Args: 
        environment_accordion (object): environment accordion contents

    Returns: 
        services_tab_content (object): dash dbc.Card() that contains all relevant accordions
    """
    environment_tab_content = dbc.Card(
        dbc.CardBody(
            [
                html.P("Constructions, pollution, noise, crime", className="card-text"),
                html.Div(),
            ]
        ),
        className="mt-3",
    )
    return environment_tab_content

def layout_main(navbar, tabs, choropleth):
    """
    """
    layout = html.Div(
        [   
            dbc.Row(
                dbc.Col(
                    html.Div(navbar),
                    width=12,
                )
            ),
            dbc.Row(   
                [
                    dbc.Col(
                        html.Div(
                            tabs, 
                            style={'height':'100vh', "overflow-y": "scroll", "overflow-x": "hidden"}),
                            width=4,
                        ),
                    dbc.Col(
                        html.Div(
                            dcc.Graph(
                                id='choropleth-map',
                                figure=choropleth,
                                config={'displayModeBar': False},
                                style={ 'height':'100vh'}
                            )
                        ),
                        width=8
                    ),
                ]
            ), 
        ]
    )
    return layout

def main():
    """
    Initialize the navbar and all tabs.
    Args: None

    Returns: 
        layout (object): Main layout of the app
    """
    datum, real_estate  = load_datum()
    real_estate_scatter = real_estate_scatter_plots(real_estate)
    choropleth = init_choropleth(datum)

    navbar = init_navbar()

    census_individuals_accordion = init_census_individual_accordion()
    census_households_accordion = init_census_household_accordion()
    census_tab_content = tab_census(census_individuals_accordion, census_households_accordion)

    real_estate_accordion = init_real_estate_accordion()
    real_estate_tab_content = tab_real_estate(real_estate_accordion, real_estate_scatter)

    service_accordion = init_services_accordion()
    services_tab_content = tab_services(service_accordion)

    mobility_accordion = init_mobility_accordion()
    mobility_tab_content = tab_mobility(mobility_accordion)

    tabs = dbc.Tabs(
        [
            dbc.Tab(census_tab_content, label="Census", disabled=False),
            dbc.Tab(real_estate_tab_content, label="Real Estate", disabled=False),
            dbc.Tab(services_tab_content, label="Services", disabled=True),
            dbc.Tab(mobility_tab_content, label="Mobility", disabled=True),
        ]
    )

    layout = layout_main(navbar, tabs, choropleth)

    return layout

layout = main()