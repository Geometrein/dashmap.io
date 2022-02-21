"""
This module creates the main Graph objects.
"""
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
        datum (object: gpd.GeoDataFrame): main geodataframe
        real_estate (object: pd.DataFrame): dataframe with real estate data
        bus_stops (object: gpd.GeoDataFrame): dataframe with real estate data
    """
    datum = gpd.read_file(open("website/data/datum/datum.geojson"), crs="WGS84")
    datum.rename(columns={'index': 'postal_code'}, inplace=True)
    datum.set_index('postal_code', inplace=True)

    real_estate = pd.read_csv('website/data/real-estate/real-estate.csv')
    real_estate.set_index('postcode', inplace=True)

    bus_stops = gpd.read_file(open("website/data/mobility/HSL_stations.geojson"), crs="WGS84")
    return datum, real_estate, bus_stops


def add_choropleth_layer(
        name: str, fig: go.Figure, df: pd.DataFrame, z_index: int,
        colorscale: str, ticksize: int, visible: str = 'legendonly') -> None:
    """
    This function adds a trace
    for plotly figure object.
    ---
    Args:
        name (str): Name of the trace
        fig (go.Figure): plotly graph object
        df (pd.DataFrame): dataframe or geodataframe
        z_index (int): Choropleth color value
        colorscale (str): Color map of color bar
        ticksize (int): Size of color bar ticks
        visible (str): Trace visibility on load. Default is 'legendonly'

    Returns:
        None
    """
    geojson = json.loads(df.to_json())
    locations = df.index
    neighborhood = df['neighborhood']
    z = df.iloc[:, z_index]

    fig.add_trace(
        go.Choroplethmapbox(
            name=name,
            geojson=geojson,
            locations=locations,
            z=z,
            colorscale=colorscale,
            colorbar=dict(
                len=0.5,
                x=0.93,
                y=0.5,
                tickfont=dict(
                    size=ticksize,
                    color="white"
                )
            ),
            marker_line_width=1,
            marker_opacity=.3,
            marker_line_color='#fff',
            visible=visible,
            hovertext=locations,
            text=neighborhood,
            hovertemplate="<b>Neighborhood:</b> %{text}<br><b>Postal Area</b>: " +
                          "%{hovertext}<br>" + f"<b>{name}: </b>" + "%{z}<br><extra></extra>"
        )
    )


def add_postal_areas(fig: go.Figure, df: pd.DataFrame) -> None:
    """
    This function adds a trace with postal districts
    for plotly figure object.
    ---
    Args:
        fig (object): plotly graph object
        df (object): dataframe or geodataframe

    Returns:
        None
    """
    fig.add_trace(
        go.Choroplethmapbox(
            name="Postal Areas",
            geojson=json.loads(df.to_json()),
            locations=df.index,
            z=df['Inhabitants, total, 2019 (HE)'],
            colorscale=["#A9A9A9", "#A9A9A9"],
            colorbar=dict(
                len=0.5,
                x=0.70,
                y=0.5,
                tickfont=dict(
                    size=1,
                    color="white"
                )
            ),
            marker_line_width=1,
            marker_opacity=.3,
            marker_line_color='#fff',
            hovertext=df.index,
            text=df['neighborhood'],
            hovertemplate="<b>Neighborhood:</b> %{text}<br>" +
                          "<b>Postal Area</b>: %{hovertext}<br><extra></extra>"
        )
    )


def add_population(fig: go.Figure, df: pd.DataFrame) -> None:
    """
    This function adds a trace with population
    for plotly figure object.
    ---
    Args:
        fig (object): plotly graph object
        df (object): dataframe or geodataframe

    Returns:
        None
    """
    fig.add_trace(
        go.Choroplethmapbox(
            name="Population",
            geojson=json.loads(df.to_json()),
            locations=df.index,
            z=df['Inhabitants, total, 2019 (HE)'],
            colorscale='blues',
            colorbar=dict(
                len=0.5,
                x=0.93,
                y=0.5,
                tickfont=dict(
                    size=10,
                    color="white"
                )
            ),
            marker_line_width=1,
            marker_opacity=.4,
            marker_line_color='#fff',
            visible='legendonly',
            hovertext=df.index,
            text=df['neighborhood'],
            hovertemplate="<b>Neighborhood:</b> %{text}<br><b>Postal Area</b>:" +
                          "%{hovertext}<br><b>Population:</b> %{z}<br><extra></extra>"
        )
    )


def add_income(fig: go.Figure, df: pd.DataFrame) -> None:
    """
    This function adds a trace with Avg. Individual Income
    for plotly figure object.
    ---
    Args:
        fig (object): plotly graph object
        df (object): dataframe or geodataframe

    Returns:
        None
    """
    # Adding Average income by postal code trace
    fig.add_trace(
        go.Choroplethmapbox(
            name="Avg. Individual Income",
            geojson=json.loads(df.to_json()),
            locations=df.index,
            z=df['Average income of inhabitants, 2019 (HR)'],
            colorscale="Bluered",
            colorbar=dict(
                len=0.5,
                x=0.93,
                y=0.5,
                tickfont=dict(
                    size=10,
                    color="white"
                )
            ),
            marker_line_width=1,
            marker_opacity=.4,
            marker_line_color='#fff',
            visible='legendonly',
            hovertext=df.index,
            text=df['neighborhood'],
            hovertemplate="<b>Neighborhood:</b> %{text}<br>" +
                          "<b>Postal Area</b>: %{hovertext}<br><b>Avg." +
                          "Individual Income:</b> %{z}<br><extra><extra></extra>"
        )
    )


def add_household_income(fig: go.Figure, df: pd.DataFrame) -> None:
    """
    This function adds a trace with Avg. Households Income
    for plotly figure object.
    ---
    Args:
        fig (object): plotly graph object
        df (object): dataframe or geodataframe

    Returns:
        None
    """
    fig.add_trace(
        go.Choroplethmapbox(
            name="Avg. Households Income",
            geojson=json.loads(df.to_json()),
            locations=df.index,
            z=df['Average income of households, 2019 (TR)'],
            colorscale="hot",
            colorbar=dict(
                len=0.5,
                x=0.93,
                y=0.5,
                tickfont=dict(
                    size=10,
                    color="white"
                )
            ),
            marker_line_width=1,
            marker_opacity=.4,
            marker_line_color='#fff',
            visible='legendonly',
            hovertext=df.index,
            text=df['neighborhood'],
            hovertemplate="<b>Neighborhood:</b> %{text}<br>" +
                          "<b>Postal Area</b>: %{hovertext}<br><b>Avg." +
                          "Households Income:</b> %{z}<br><extra></extra>"
        )
    )


def add_avg_age(fig: go.Figure, df: pd.DataFrame) -> None:
    """
    This function adds a trace with Avg. Inhabitant Age
    for plotly figure object.
    ---
    Args:
        fig (object): plotly graph object
        df (object): dataframe or geodataframe

    Returns:
        None
    """
    z = df['Average age of inhabitants, 2019 (HE)']
    fig.add_trace(
        go.Choroplethmapbox(
            name="Avg. Inhabitant Age",
            geojson=json.loads(df.to_json()),
            locations=df.index,
            z=z,
            colorscale="tealgrn",
            colorbar=dict(
                len=0.5,
                x=0.93,
                y=0.5,
                tickfont=dict(
                    size=10,
                    color="white"
                )
            ),
            marker_line_width=1,
            marker_opacity=.4,
            marker_line_color='#fff',
            visible='legendonly',
            hovertext=df.index,
            text=df['neighborhood'],
            hovertemplate="<b>Neighborhood:</b> %{text}<br><b>Postal Area</b>:" +
                          "%{hovertext}<br><b>Avg. Age:</b> %{z}<br><extra></extra>"
        )
    )


def add_avg_household_size(fig: go.Figure, df: pd.DataFrame) -> None:
    """
    This function adds a trace with Avg. Household Size
    for plotly figure object.
    ---
    Args:
        fig (object): plotly graph object
        df (object): dataframe or geodataframe

    Returns:
        None
    """
    fig.add_trace(
        go.Choroplethmapbox(
            name="Avg. Household Size",
            geojson=json.loads(df.to_json()),
            locations=df.index,
            z=df['Average size of households, 2019 (TE)'],
            colorscale="aggrnyl",
            colorbar=dict(
                len=0.5,
                x=0.93,
                y=0.5,
                tickfont=dict(
                    size=10,
                    color="white"
                )
            ),
            marker_line_width=1,
            marker_opacity=.4,
            marker_line_color='#fff',
            visible='legendonly',
            hovertext=df.index,
            text=df['neighborhood'],
            hovertemplate="<b>Neighborhood:</b> %{text}<br><b>Postal Area</b>:" +
                          "%{hovertext}<br><b>Avg. Household size:</b> %{z}<br><extra></extra>"
        )
    )
    return fig


def add_mobility_nodes(fig: go.Figure, df: pd.DataFrame) -> None:
    """
    This function adds a trace with Mobility Nodes
    for plotly figure object.
    ---
    Args:
        fig (object): plotly graph object
        df (object): dataframe or geodataframe

    Returns:
        None
    """
    fig.add_trace(
        go.Scattermapbox(
            name="Mobility Network",
            lat=df['geometry'].y,
            lon=df['geometry'].x,
            hovertext=df['NAMN1'],
            marker=go.scattermapbox.Marker(color=colors[1], size=5),
            marker_opacity=.65,
            visible='legendonly',
            text=df['NAMN1'],
            hovertemplate="<b>Name:</b> %{text}<br><extra></extra>"
        )
    )


def update_layout_and_traces(fig: go.Figure) -> object:
    """
    This function updates layout preferences
    for plotly figure object.
    ---
    Args:
        fig (object): plotly graph object

    Returns:
        fig (object): Plotly Graph Object
    """
    fig.update_layout(
        clickmode='event+select',
        mapbox_style="dark",

        autosize=True,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor='#303030',
        plot_bgcolor='#303030',
        legend=dict(
            x=0.02,
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
    fig.update_traces(
        showlegend=True,
        selector=dict(type='choroplethmapbox'),
        unselected=dict(marker={'opacity': 0.2}),
        selected=dict(marker={'opacity': 0.5})
    )

    return fig


def save_image(fig: go.Figure, width: int = 3840, height: int = 2160) -> None:
    """
    Save figure as an image file
    ---
    Args:
        fig (object): plotly graph object
        width (int): width in pixels
        height (int): height in pixels

    Returns:
        None
    """
    fig.write_image(
        "fig.png",
        width=width,
        height=height,
        scale=1,
        engine='kaleido'
    )


def init_choropleth(df: pd.DataFrame, df_mobility: pd.DataFrame) -> object:
    """
    Initialize the main choropleth map.
    ---
    Args:
        df (pd.DataFrame): DataFrame containing census data
        df_mobility (pd.DataFrame): DataFrame containing bus stops data
    Returns:
        choropleth (go.Figure): Plotly Graph Object
    """
    # Initializing an empty graph object
    choropleth = go.Figure()

    add_choropleth_layer(
        name="Postal Areas",
        fig=choropleth,
        df=df,
        z_index=3,
        colorscale=["#A9A9A9", "#A9A9A9"],
        ticksize=1,
        visible=True
    )

    add_choropleth_layer(
        name="Population",
        fig=choropleth,
        df=df,
        z_index=3,
        colorscale='blues',
        ticksize=10,
    )

    add_choropleth_layer(
        name="Avg. Individual Income",
        fig=choropleth,
        df=df,
        z_index=35,
        colorscale='Bluered',
        ticksize=10,
    )

    add_choropleth_layer(
        name="Avg. Households Income",
        fig=choropleth,
        df=df,
        z_index=59,
        colorscale='hot',
        ticksize=10,
    )

    add_choropleth_layer(
        name="Avg. Household Size",
        fig=choropleth,
        df=df,
        z_index=42,
        colorscale='aggrnyl',
        ticksize=10,
    )

    add_mobility_nodes(choropleth, df_mobility)

    # Update Layout
    update_layout_and_traces(choropleth)

    return choropleth
