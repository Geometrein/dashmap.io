import os
import json
import pandas as pd
import geopandas as gpd

# Dash & Plotly
from dash import html
from dash import dcc
import plotly.graph_objects as go

# Environment Variables
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('MAPBOX_TOKEN')

# Colors used by graphs
colors = [
    '#4182C8', '#2E94B2',
    '#39A791', '#6FB26C',
    '#C0C15C', '#F9BD24',
    '#F3903F', '#EC6546',
    '#7D4C94', '#5B61AE'
]

def load_datum():
    """
    Load the main data sources.
    Args: None

    Returns: 
        datum (object): main geodataframe
        real_estate (object): dataframe with real estate data
    """
    datum = gpd.read_file(open("website/data/datum/datum.geojson"), crs="WGS84")
    datum.rename(columns = {'index': 'postal_code'}, inplace = True)
    datum.set_index('postal_code', inplace=True)
    #print(len(datum.index), len(datum), datum.head())

    real_estate = pd.read_csv('website/data/real-estate/real-estate.csv')
    real_estate.set_index('postcode', inplace=True)

    return datum, real_estate

def init_choropleth(datum):
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

def real_estate_scatter_plots(dataframe):
    """
    Initialize the scatterplots on Real estate page.
    ---
    Args: 
        dataframe (object): Pandas dataframe with relevant information.

    Returns: 
        children (list): list of dash html components
    """
    df = dataframe[dataframe['deal_type']=='rent']
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

    df = dataframe[dataframe['deal_type']=='sell']
    df = df[df['price']<2000000]
    df = df[df['area']<310]

    x = df['area']
    y = df['price']

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

