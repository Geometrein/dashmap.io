import os
import json
import pandas as pd
import geopandas as gpd

# Dash & Plotly
import plotly.graph_objects as go

# Environment Variables
from dotenv import load_dotenv
load_dotenv()
MAPBOX_TOKEN = os.getenv('MAPBOX_TOKEN')

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
        datum (object: geopandas geodataframe): main geodataframe
        real_estate (object: pandas dataframe): dataframe with real estate data
        bus_stops (object: geopandas geodataframe): dataframe with real estate data
    """
    datum = gpd.read_file(open("website/data/datum/datum.geojson"), crs="WGS84")
    datum.rename(columns = {'index': 'postal_code'}, inplace = True)
    datum.set_index('postal_code', inplace=True)
    #print(len(datum.index), len(datum), datum.head())

    real_estate = pd.read_csv('website/data/real-estate/real-estate.csv')
    real_estate.set_index('postcode', inplace=True)

    bus_stops = gpd.read_file(open("website/data/mobility/HSL_stations.geojson"), crs="WGS84")

    return datum, real_estate, bus_stops

def init_choropleth(datum: object, bus_stops: object) -> object:
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
            locations=datum.index,
            z=datum['Inhabitants, total, 2019 (HE)'],
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

    # Adding Population
    choropleth.add_trace(
        go.Choroplethmapbox(
            name="Population",
            geojson=json.loads(datum.to_json()), 
            locations=datum.index,
            z=datum['Inhabitants, total, 2019 (HE)'],
            colorscale='blues',
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
            hovertemplate = "<b>Neighborhood:</b> %{text}<br><b>Postal Area</b>: %{hovertext}<br><b>Population:</b> %{z}<br><extra></extra>"
        )
    )

    # Adding Average income by postal code trace
    choropleth.add_trace(
        go.Choroplethmapbox(
            name="Avg. Individual Income",
            geojson=json.loads(datum.to_json()), 
            locations=datum.index,
            z=datum['Average income of inhabitants, 2019 (HR)'],
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
            marker_opacity=.4,
            marker_line_color= '#fff',
            visible='legendonly',
            hovertext = datum.index,
            text = datum['neighborhood'],
            hovertemplate = "<b>Neighborhood:</b> %{text}<br><b>Postal Area</b>: %{hovertext}<br><b>Avg. Individual Income:</b> %{z}<br><extra><extra></extra>"
        )
    )

    # Adding Avg. Households Income by postal code trace
    choropleth.add_trace(
        go.Choroplethmapbox(
            name="Avg. Households Income",
            geojson=json.loads(datum.to_json()), 
            locations=datum.index,
            z=datum['Average income of households, 2019 (TR)'],
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
            hovertemplate = "<b>Neighborhood:</b> %{text}<br><b>Postal Area</b>: %{hovertext}<br><b>Avg. Households Income:</b> %{z}<br><extra></extra>"
        )
    )

    # Adding Avg. Inhabitant Age by postal code trace
    choropleth.add_trace(
        go.Choroplethmapbox(
            name="Avg. Inhabitant Age",
            geojson=json.loads(datum.to_json()), 
            locations=datum.index,
            z=datum['Average age of inhabitants, 2019 (HE)'],
            colorscale="tealgrn",
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
            hovertemplate = "<b>Neighborhood:</b> %{text}<br><b>Postal Area</b>: %{hovertext}<br><b>Avg. Age:</b> %{z}<br><extra></extra>"
        )
    )

    # Adding Avg. Household Size by postal code trace
    choropleth.add_trace(
        go.Choroplethmapbox(
            name="Avg. Household Size",
            geojson=json.loads(datum.to_json()), 
            locations=datum.index,
            z=datum['Average size of households, 2019 (TE)'],
            colorscale="aggrnyl",
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
            hovertemplate = "<b>Neighborhood:</b> %{text}<br><b>Postal Area</b>: %{hovertext}<br><b>Avg. Household size:</b> %{z}<br><extra></extra>"
        )
    )

    # Adding Mobility Nodes
    choropleth.add_trace(
        go.Scattermapbox(
            name="Mobility Network",
            lat = bus_stops['geometry'].y,
            lon = bus_stops['geometry'].x,
            hovertext = bus_stops['NAMN1'],
            marker = go.scattermapbox.Marker(color=colors[1],size=5),
            marker_opacity=.6,
            visible='legendonly',
            text = bus_stops['NAMN1'],
            hovertemplate = "<b>Name:</b> %{text}<br><extra></extra>"
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
            accesstoken=MAPBOX_TOKEN,
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
        unselected= dict(marker={'opacity': 0.2}),
        selected= dict(marker={'opacity': 0.5})
    )

    return choropleth

