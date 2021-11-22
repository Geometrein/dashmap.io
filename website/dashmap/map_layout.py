# Dash and Plotly
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

# Plotly Graph Objects
from .map_graphs import *

# Each tab contents
from .layouts.tab_census.main_census import init_tab_census
from .layouts.tab_real_estate.main_real_estate import init_tab_real_estate
from .layouts.tab_services.main_services import init_tab_services
from .layouts.tab_mobility.main_mobility import init_tab_mobility
from .layouts.tab_environment.main_environment import init_tab_environment

from .layouts.navbar.navbar import init_navbar

def layout_main(navbar, tabs, choropleth):
    """
    Create the main app layout.
    Args: 
        navbar (object): dash bootstrap component NavbarSimple() with navigation components
        tabs (object): dash bootstrap component dbc.Tabs() with all content tabs
        choropleth (object): Plotly Graph Object go.Choroplethmapbox()
        
    Returns: 
        layout (object): dash html.Div() that contains all components for dash app layout
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

def init_layout():
    """
    Initialize the navbar and all tabs.
    Args: None

    Returns: 
        layout (object): Main layout of the app
    """
    datum, real_estate, bus_stops  = load_datum()
    choropleth = init_choropleth(datum, bus_stops)

    navbar = init_navbar()

    census_tab_content = init_tab_census()
    real_estate_tab_content = init_tab_real_estate()
    services_tab_content =  init_tab_services()
    mobility_tab_content = init_tab_mobility()
    environment_tab_content = init_tab_environment()

    tabs = dbc.Tabs(
        [
            dbc.Tab(census_tab_content, label="Census", disabled=False),
            dbc.Tab(real_estate_tab_content, label="Real Estate", disabled=False),
            dbc.Tab(services_tab_content, label="Services", disabled=False),
            dbc.Tab(mobility_tab_content, label="Mobility", disabled=False),
            dbc.Tab(environment_tab_content, label="Environment", disabled=False),
        ]
    )

    return layout_main(navbar, tabs, choropleth)

layout = init_layout()