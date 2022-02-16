import pandas as pd
from dash import html
from dash import dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from ...callbacks.util.helpers import privacy_check, privacy_notice, get_postal_code

colors = [
    '#4182C8', '#2E94B2',
    '#39A791', '#6FB26C',
    '#C0C15C', '#F9BD24',
    '#F3903F', '#EC6546',
    '#7D4C94', '#5B61AE'
]

def init_mobility_callbacks(app, datum):
    """
    """
    # Tab 4 Section 1 mobility CallBack
    @app.callback(
        Output('id_mobility_index', 'children'),
        Input('choropleth-map', 'clickData'))
    def display_click_data(click_data):
        """
        Generates the graphs for mobility index section.
        ---
        Args: 
            click_data (dict): dictionary returned by dcc.Graph component triggered by user-interaction.

        Returns: 
            children (list): List of html components to be displayed.
        """
        section_title = "Mobility Index"

        # Get the postal code based on clicked area
        postal_code = get_postal_code(click_data)

        # Get df row based on postal number
        result = datum.loc[postal_code]
        neighborhood = result['neighborhood']

        mobility_data = pd.read_csv('website/data/mobility/mobility.csv', dtype='str')
        mobility_data.set_index('index', inplace=True)

        mobility_data = mobility_data.loc[postal_code]
        mobility_index = float(mobility_data['mobility_index'])
        surface_area = float(mobility_data['Surface area'])/1000
        mobility_nodes = float(mobility_data['mobility_nodes'])

        # Data privacy check
        if privacy_check(postal_code):
            return privacy_notice(section_title, neighborhood)

        fig = go.Figure()

        fig.add_trace(go.Indicator(
            mode="number",
            value=mobility_index,
            number={'prefix': ""},
            title={"text": f"Mobility Index<br><span style='font-size:0.8em;color:gray'>" +
                           "index is a value between 1 and 0</span><br>"},
            )
        )
        
        fig.update_layout(
            paper_bgcolor='#1E1E1E',
            plot_bgcolor='#1E1E1E',
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            autosize=True,
            font=dict(color="white")
        )

        text_pre = f"""
        Dashmap mobility index is a composite index that indicates how well the given area is connected to
        other areas within the city. The index takes into account various factors including the surface area
        of the region, number of public transit routes and their relationships with each other. The higher the
        index the better the connectivity of the given area.
        """

        text_post = f"""
        Dashmap mobility index for {neighborhood} neighborhood is {mobility_index:.3f}.
        Dashmap mobility index is a composite index that indicates how well is the area connected to
        other areas within the city. The index takes into account various factors including the surface area,
        number of bus, tram and metro stations and their relationships with each other.
        {neighborhood} neighborhood has a surface area of {surface_area:.1f} km²
        and {mobility_nodes:.0f} mobility nodes.
        """

        children = [
            html.H4(section_title),
            html.Hr(),
            html.P(text_pre),
            dcc.Graph(id='injected5', figure=fig, config={'displayModeBar': False}),
            html.P(text_post),
        ]
        return children


    # Tab 5 Section 1 Windrose CallBack
    @app.callback(
        Output('id_windrose', 'children'),
        Input('choropleth-map', 'clickData'))
    def display_click_data(click_data):
        """
        Generates the graphs for Bus section.
        ---
        Args: 
            click_data (dict): dictionary returned by dcc.Graph component triggered by user-interaction.

        Returns: 
            children (list): List of html components to be displayed.
        """
        section_title = "Wind Patterns"

        text = f"""
        Wind is the natural movement of air or other gases relative to a planet's surface.
        They are commonly classified by their spatial scale, their speed and direction, the forces that cause them,
        the regions in which they occur, and their effect. Regional wind patterns could either facilitate or hinder 
        some of the social and biological processes, depending on the alignment of winds with other
        spatial climate patterns.
        """

        df = pd.read_csv("website/data/environment/air-temperature-wind/wind_data.csv")

        r_1 = df['r_1'].to_list()
        r_2 = df['r_2'].to_list()
        r_3 = df['r_3'].to_list()
        r_4 = df['r_4'].to_list()

        fig = go.Figure()
        fig.add_trace(
            go.Barpolar(
                r=r_1,
                name='< 5 m/s',
                marker_color=colors[3]
            )
        )
        fig.add_trace(
            go.Barpolar(
                r=r_2,
                name='5-8 m/s',
                marker_color=colors[2]
            )
        )
        fig.add_trace(
            go.Barpolar(
                r=r_3,
                name='8-10 m/s',
                marker_color=colors[1]
            )
        )
        fig.add_trace(
            go.Barpolar(
                r=r_4,
                name='> 11 m/s',
                marker_color=colors[8]
            )
        )
        fig.update_layout(
            font=dict(
                size=14,
                color="#fff"
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5,
            ),
            legend_font_size=12,
            polar_radialaxis_ticksuffix='%',
            polar_angularaxis_rotation=0,
            paper_bgcolor='#1E1E1E', 
            plot_bgcolor='#1E1E1E',
            margin={"r": 30, "t": 30, "l": 30, "b": 30},
            autosize=True
        )

        fig.update_polars(bgcolor='#1E1E1E')

        children = [
            html.H4(section_title),
            dcc.Graph(id='injected5', figure=fig, config={'displayModeBar': False}),
            html.P(text),
        ]
        return children