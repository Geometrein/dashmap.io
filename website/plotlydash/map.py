import os
import json
import pandas as pd
import geopandas as gpd

# Dash and Plotly
from dash import Dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Dash Callbacks
from  .map_callbacks import init_callbacks

# Environment Variables
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('MAPBOX_TOKEN')

# Color pallete used is graphs
colors=[
    '#4182C8', '#2E94B2', '#39A791',
    '#6FB26C', '#C0C15C', '#F9BD24',
    '#F3903F', '#EC6546', '#7D4C94',
    '#5B61AE'
]

#####################################################################################################################
#                                                Data                                                               #
#####################################################################################################################
def load_datum():
    """
    Load the main GeoDataFrame.
    Args: None

    Returns: 
        choropleth (object): Plotly Graph Object

    """
    datum = gpd.read_file(open("website/data/datum/datum.geojson"), crs="WGS84")
    datum.rename(columns = {'index': 'postal_code'}, inplace = True)
    datum.set_index('postal_code', inplace=True)
    #print(len(datum.index), len(datum), datum.head())

    real_estate = pd.read_csv('website/data/real-estate/real-estate.csv')
    real_estate.set_index('postcode', inplace=True)

    return datum, real_estate
    
# Load the main GeoDataFrame.
datum, real_estate = load_datum()
#####################################################################################################################
#                                           Choropleth MAP                                                          #
#####################################################################################################################

def init_choropleth():
    """
    Initialize the main choropleth map.
    ---
    Args: None

    Returns: 
        choropleth (object): Plotly Graph Object
    """
    # Initializing the Figure
    choropleth = go.Figure()

    # Adding postal districts trace
    choropleth.add_trace(
        go.Choroplethmapbox(
            name="Postal Areas",
            geojson=json.loads(datum.to_json()), 
            locations=datum.index, z=datum['Inhabitants, total, 2019 (HE)'],
            colorscale=["#A9A9A9", "#A9A9A9"],
            colorbar=dict(
                len=1, 
                x=0.95,
                y=0.5, 
                tickfont=dict(
                    size=10, 
                    color= "white"
                )
            ),
            marker_line_width=1,
            marker_opacity=.3,
            marker_line_color= '#fff',
            hovertext = datum.index,
            text = datum['neighborhood'],
            hovertemplate = "<b>Neighborhood:</b> %{text}<br><b>Postal Area</b>: %{hovertext}<br><extra></extra>"
        )
    )

    # Adding Average income by postal code trace
    choropleth.add_trace(
        go.Choroplethmapbox(
            name="Avg. Individual Income",
            geojson=json.loads(datum.to_json()), 
            locations=datum.index, z=datum['Average income of inhabitants, 2019 (HR)'],
            colorscale="Bluered",
            colorbar=dict(
                len=1, 
                x=0.95,
                y=0.5, 
                tickfont=dict(
                    size=10, 
                    color= "white"
                )
            ),
            marker_line_width=1,
            marker_opacity=.2,
            marker_line_color= '#fff',
            visible='legendonly',
            hovertext = datum.index,
            text = datum['neighborhood'],
            hovertemplate = "<b>Neighborhood:</b> %{text}<br><b>Postal Area</b>: %{hovertext}<br><extra></extra>"
        )
    )

    # Adding Avg. Households Income by postal code trace
    choropleth.add_trace(
        go.Choroplethmapbox(
            name="Avg. Households Income",
            geojson=json.loads(datum.to_json()), 
            locations=datum.index, z=datum['Average income of households, 2019 (TR)'],
            colorscale="hot",
            colorbar=dict(
                len=1, 
                x=0.95,
                y=0.5, 
                tickfont=dict(
                    size=10, 
                    color= "white"
                )
            ),
            marker_line_width=1,
            marker_opacity=.4,
            marker_line_color= '#fff',
            visible='legendonly',
            hovertext = datum.index,
            text = datum['neighborhood'],
            hovertemplate = "<b>Neighborhood:</b> %{text}<br><b>Postal Area</b>: %{hovertext}<br><extra></extra>"
        )
    )

    # Adding Avg. Inhabitant Age by postal code trace
    choropleth.add_trace(
        go.Choroplethmapbox(
            name="Avg. Inhabitant Age",
            geojson=json.loads(datum.to_json()), 
            locations=datum.index, z=datum['Average age of inhabitants, 2019 (HE)'],
            colorscale="hot",
            colorbar=dict(
                len=1, 
                x=0.95,
                y=0.5, 
                tickfont=dict(
                    size=10, 
                    color= "white"
                )
            ),
            marker_line_width=1,
            marker_opacity=.4,
            marker_line_color= '#fff',
            visible='legendonly',
            hovertext = datum.index,
            text = datum['neighborhood'],
            hovertemplate = "<b>Neighborhood:</b> %{text}<br><b>Postal Area</b>: %{hovertext}<br><extra></extra>"
        )
    )

    # Adding Avg. Household Size by postal code trace
    choropleth.add_trace(
        go.Choroplethmapbox(
            name="Avg. Household Size",
            geojson=json.loads(datum.to_json()), 
            locations=datum.index, z=datum['Average size of households, 2019 (TE)'],
            colorscale="hot",
            colorbar=dict(
                len=1, 
                x=0.95,
                y=0.5, 
                tickfont=dict(
                    size=10, 
                    color= "white"
                )
            ),
            marker_line_width=1,
            marker_opacity=.4,
            marker_line_color= '#fff',
            visible='legendonly',
            hovertext = datum.index,
            text = datum['neighborhood'],
            hovertemplate = "<b>Neighborhood:</b> %{text}<br><b>Postal Area</b>: %{hovertext}<br><extra></extra>"
        )
    )

    # Update layout preferences
    choropleth.update_layout(
        clickmode='event+select',
        mapbox_style="dark",
        
        autosize=True,
        margin={"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor='#303030',
        plot_bgcolor='#303030',
        legend=dict(x=0.02,
            y=0.99,
            yanchor="top",
            orientation="v",
            font=dict(
                family="Courier",
                size=12,
                color="white"
            )
        ),
        mapbox=dict(   
            accesstoken=token,
            bearing=0,
            center=dict(lat=60.192059, lon=24.945831),
            pitch=3,
            zoom=10,
        ),
    )

    # Update Trace preferences
    choropleth.update_traces(
        showlegend=True,
        selector=dict(type='choroplethmapbox'),
        unselected= dict(marker={'opacity': 0.15}),
        selected= dict(marker={'opacity': 0.4})
    )

    return choropleth

# Initialize the main choropleth map.
choropleth = init_choropleth()

def real_estate_scatter(real_estate):
    """
    """
    df = real_estate[real_estate['deal_type']=='rent']
    df = df[df['price']<5000]
    df = df[df['area']<310]

    y = df['price']
    x = df['area']

    scatter_chart_rent = go.Figure(
        data=go.Scattergl(
            x = x,
            y = y,
            mode='markers',
            marker=dict(
                size=8,
                color=df['rooms'],
                colorscale='OrYel', # one of plotly colorscales
                showscale= True,
                
            ),
        )
    )

    scatter_chart_rent.update_layout(
        showlegend=False,
        paper_bgcolor='#1E1E1E',
        plot_bgcolor='#1E1E1E',
        margin={"r":50,"t":50,"l":50,"b":50},
        autosize=True,
    )
    scatter_chart_rent.update_traces(marker=dict(line=dict(color='#1E1E1E', width=3)))
    scatter_chart_rent.update_xaxes(color='#fff', gridcolor='#D3D3D3')
    scatter_chart_rent.update_yaxes(color='#fff', gridcolor='#D3D3D3')

    df = real_estate[real_estate['deal_type']=='sell']
    df = df[df['price']<2000000]
    df = df[df['area']<310]

    y = df['price']
    x = df['area']
    scatter_chart_sell = go.Figure(
        data=go.Scattergl(
            x = x,
            y = y,
            mode='markers',
            marker=dict(
                size=8,
                color=df['rooms'],
                colorscale='tealgrn', # one of plotly colorscales
                showscale= True,
            )
        )
    )

    scatter_chart_sell.update_layout(showlegend=False, paper_bgcolor='#1E1E1E', plot_bgcolor='#1E1E1E', margin={"r":50,"t":50,"l":50,"b":50}, autosize=True,)
    scatter_chart_sell.update_traces(marker=dict(line=dict(color='#1E1E1E', width=3)))
    scatter_chart_sell.update_xaxes(color='#fff', gridcolor='#D3D3D3')
    scatter_chart_sell.update_yaxes(color='#fff', gridcolor='#D3D3D3')

    children=[
        html.H5("Price vs Square Meters"),
        html.P(
            """
            Scatterplots below hels us understand the relationships between Apartment area and its price.
            """
        ),
        html.H5("Rental Apartments"),
        dcc.Graph(id='real_estate_scatter_rent', figure=scatter_chart_rent, config={'displayModeBar': False}),
        html.H5("Owned Apartments"),
        dcc.Graph(id='real_estate_scatter_sell', figure=scatter_chart_sell, config={'displayModeBar': False}),
    ]

    return children

real_estate_scatter = real_estate_scatter(real_estate)

#####################################################################################################################
#                                              NAVIGATION                                                           #
#####################################################################################################################

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

footer = html.P(
    "Created by Tigran Khachatryan │ Data was provided by Statistics Finland under CC BY 4.0 license │ ",
    style = {'margin-left': '50px',
        'font-family': '',
        'font-size': '2',
        'font-weight': '10',
        'line-height': '15px',
        'color': '#fff',
        'text-align': 'left',}
)

#####################################################################################################################
#                                         Tab-CENSUS-individual-accordions                                          #
#####################################################################################################################

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

#####################################################################################################################
#                                         Tab-CENSUS-Household-accordions                                           #
#####################################################################################################################

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

#####################################################################################################################
#                                         Tab-Real-Estate-accordions                                                #
#####################################################################################################################

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

#####################################################################################################################
#                                                  Accordions Groups                                                #
#####################################################################################################################

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

census_households_accordion = html.Div(
    [
        accord_household_size,
        accord_household_structure,
        accord_household_income,
        accord_household_dwell
    ],
    className="accordion"
)

real_estate_accordion = html.Div(
    [
        accord_re_renting,
        accord_re_owning,
        accord_re_sauna
    ],
    className="accordion"
)

mobility_accordion = html.Div(
    [

    ],
    className="accordion"
)

#####################################################################################################################
#                                                  Main Tabs                                                        #
#####################################################################################################################

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

environment_tab_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("Constructions, pollution, noise, crime", className="card-text"),
            html.Div(),
        ]
    ),
    className="mt-3",
)



tabs = dbc.Tabs(
    [
        dbc.Tab(census_tab_content, label="Census", disabled=False),
        dbc.Tab(real_estate_tab_content, label="Real Estate", disabled=False),
        dbc.Tab(services_tab_content, label="Services", disabled=True),
        dbc.Tab(mobility_tab_content, label="Mobility", disabled=True),
    ]
)

#####################################################################################################################
#                                                  APP LAYOUT      ༼ つ ◕_◕ ༽つ                                      #
#####################################################################################################################
          
def init_dashboard(server):
    """
    Initialize the dashboard.
    ---
    Args:
        server: the main Flask app

    Returns: dash app
    """
    # Initialize the Dash app
    dash_app = Dash(
        __name__,
        title="Dashmap",
        server=server,
        url_base_pathname='/helsinki/'
    )

    # Create the App Layout
    dash_app.layout = html.Div(
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

    # Initialize callbacks after our app is loaded
    init_callbacks(dash_app)

    return dash_app.server



    