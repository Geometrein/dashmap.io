import pandas as pd

import dash
from dash import html
from dash import dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output

colors = [
    '#4182C8', '#2E94B2',
    '#39A791', '#6FB26C',
    '#C0C15C', '#F9BD24',
    '#F3903F', '#EC6546',
    '#7D4C94', '#5B61AE'
]


def init_env_callbacks(app: dash.Dash):
    """
    Tab 5 Section 1 air temp CallBack
    """
    @app.callback(
        Output('id_air_temperature', 'children'),
        Input('choropleth-map', 'clickData')
    )
    def display_click_data(click_data: dict) -> list:
        """
        Generates the graphs for Bus section.
        ---
        Args:
            click_data (dict): dictionary returned by dcc.Graph component triggered by user-interaction.

        Returns:
            children (list): List of html components to be displayed.
        """
        section_title = "Average Air Temperature"

        text = f"""
        Air temperature indirectly affects functioning, growth, and reproduction of a wide range of
        biological and societal processes, Air temperature also affects nearly all other weather parameters
        including, air temperature affects the rate of evaporation, relative humidity, wind patterns.
        """
        df = pd.read_csv("website/data/environment/air-temperature-wind/air_temp_data.csv")

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df['month'],
                y=df['air_temp'],
                line=dict(color=colors[5], width=4),
                line_shape='spline'
            )
        )

        fig.update_layout(
                xaxis=dict(
                    tickmode='array',
                    tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                ),
                font=dict(size=14, color="#fff"),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.25,
                    xanchor="center",
                    x=0.5),
                legend_font_size=12,
                paper_bgcolor='#1E1E1E',
                plot_bgcolor='#1E1E1E',
                margin={"r": 30, "t": 30, "l": 30, "b": 30},
                autosize=True
        )

        children = [
            html.H4(section_title),
            html.Hr(),
            dcc.Graph(id='injected99', figure=fig, config={'displayModeBar': False}),
            html.P(text),
        ]
        return children

    # Tab 5 Section 2 air pollution CallBack
    @app.callback(
        Output('id_air_pollution', 'children'),
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
        section_title = "Air Pollution"

        df = pd.read_csv("website/data/environment/air-quality/air_quality_2020_clean.csv")

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df['Date'],
                y=df['Nitrogen dioxide (ug/m3)'],
                mode='lines',
                line_shape='spline',
                name='Nitrogen dioxide (ug/m3)'
            )
        )

        fig.add_trace(
            go.Scatter(
                x=df['Date'],
                y=df['Nitrogen monoxide (ug/m3)'],
                mode='lines',
                line_shape='spline',
                name='Nitrogen monoxide (ug/m3)'
            )
        )

        fig.add_trace(
            go.Scatter(
                x=df['Date'],
                y=df['Particulate matter < 10 µm (ug/m3)'],
                mode='lines',
                line_shape='spline',
                name='Particulate matter < 10 µm (ug/m3)'
            )
        )

        fig.add_trace(
            go.Scatter(
                x=df['Date'],
                y=df['Particulate matter < 2.5 µm (ug/m3)'],
                mode='lines',
                line_shape='spline',
                name='Particulate matter < 2.5 µm (ug/m3)'
            )
        )

        fig.update_layout(
            font=dict(size=14, color="#fff"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.5,
                xanchor="center",
                x=0.5,
            ),
            legend_font_size=12,
            paper_bgcolor='#1E1E1E', 
            plot_bgcolor='#1E1E1E', 
            margin={"r": 30, "t": 30, "l": 30, "b": 30},
            autosize=True
        )

        text = f"""
        Air pollution refers to the release of pollutants into the air.
        High level of pollutants in ambient air are detrimental to human health and the planet as a whole.
        Pollutants are measured in micrograms of gaseous pollutant per cubic meter of ambient air (µg/m3).
        """

        children = [
            html.H4(section_title),
            html.Hr(),
            dcc.Graph(id='injected99', figure=fig, config={'displayModeBar': False}),
            html.P(text),
        ]

        return children
