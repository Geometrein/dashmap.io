import pandas as pd
from dash import html
from dash import dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from ...callbacks.util.helpers import privacy_check, privacy_notice, get_postal_code

def init_re_callbacks(app, real_estate: pd.DataFrame):
    """
    """
    # Tab 2 Section 1 Rental Dwellings
    @app.callback(
        Output('id_re_renting', 'children'),
        Input('choropleth-map', 'clickData'))
    def display_click_data(click_data):
        """
        Generates the graphs for rental Dwellings section.
        ---
        Args:
            click_data (dict): dictionary returned by dcc.Graph component triggered by user-interaction.
        Returns:
            children (list): List of html components to be displayed.
        """
        section_title = "Rental Apartments"

        # Get the postal code based on clicked area
        postal_code = get_postal_code(click_data)

        rentals = real_estate[real_estate['deal_type'] == 'rent']

        rentals['price_per_square'] = (rentals['price'] / rentals['area'])

        # Get df row based on postal number
        if postal_code in rentals.index:
            df = rentals.loc[postal_code]
        else:
            df = pd.DataFrame(0.0, columns=rentals.columns, index=rentals.index)
            
        try:
            neighborhood = df['neighborhood'].values[0]

        except AttributeError:
            neighborhood = df['neighborhood']

        finally:
            neighborhood = ""

        price_per_square = df['price_per_square'].mean()
        average_area = df['area'].mean()
        hels_avg_price_per_square = rentals['price_per_square'].mean()
        hels_avg_re_area = rentals['area'].mean()

        rent_indicators = go.Figure()

        rent_indicators.add_trace(go.Indicator(
            mode="number",
            value=price_per_square,
            number={'prefix': "€", "font": {"size": 40}},
            title={"text": f"Rent per m² in {neighborhood}<br><span style='font-size:0.8em;color:gray'>" +
                           "Average monthly rent by square meter</span><br>"},
            domain={'x': [0, 0.5], 'y': [0.5, 1]}
            )
        )

        rent_indicators.add_trace(go.Indicator(
            mode="number",
            value=hels_avg_price_per_square,
            number={'prefix': "€", "font": {"size": 40}},
            title={"text": "Average Rent in Helsinki<br><span style='font-size:0.8em;color:gray'>" +
                           "Average monthly rent by square meter for Helsinki </span><br>"},
            domain={'x': [0.5, 1], 'y': [0.5, 1]},
            )
        )

        rent_indicators.add_trace(go.Indicator(
            mode="number",
            value=hels_avg_re_area,
            number={'suffix': " m²", "font": {"size": 40}},
            title={"text": "Average Area in Helsinki<br><span style='font-size:0.8em;color:gray'>" +
                           "All apartments average.</span><br>"},
            domain={'x': [0.5, 1], 'y': [0, .5]},
            )
        )
        rent_indicators.add_trace(
            go.Indicator(
                mode="number",
                value=average_area,
                number={'suffix': " m²", "font": {"size": 40}},
                title={"text": f"Average area in {neighborhood}<br><span style='font-size:0.8em;color:gray'>" +
                               "All apartments average.</span><br>"},
                domain={'x': [0, 0.5], 'y': [0, 0.5]},
            )
        )

        rent_indicators.update_layout(
                paper_bgcolor='#1E1E1E',
                plot_bgcolor='#1E1E1E',
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                autosize=True,
                font=dict(color="white")
        )

        # Area VS Rent Scatter Plot
        rental_df = real_estate[real_estate['deal_type'] == 'rent']
        rental_df = rental_df[rental_df['price'] < 5000]
        rental_df = rental_df[rental_df['area'] < 310]

        y = rental_df['price']
        x = rental_df['area']

        scatter_chart_rent = go.Figure(
            data=go.Scattergl(
                x=x,
                y=y,
                mode='markers',
                hovertemplate='<b>Price</b>: €%{y:.2f}' +
                '<br><b>Area</b>: %{x}m²<br>',
                marker=dict(
                    size=8,
                    color=rental_df['rooms'],
                    colorscale='OrYel',
                    showscale=True,
                ),
            )
        )

        scatter_chart_rent.update_layout(
            showlegend=False,
            paper_bgcolor='#1E1E1E',
            plot_bgcolor='#1E1E1E',
            margin={"r": 50, "t": 50, "l": 50, "b": 50},
            autosize=True,
        )

        scatter_chart_rent.update_traces(marker=dict(line=dict(color='#1E1E1E', width=3)))
        scatter_chart_rent.update_xaxes(color='#fff', gridcolor='#D3D3D3')
        scatter_chart_rent.update_yaxes(color='#fff', gridcolor='#D3D3D3')

        children = [
            html.H5(section_title),
            html.P(
                """
                Residential rental property refers to homes that are purchased by an 
                individual and inhabited by tenants on a lease or other type of rental agreement. 
                Residential property is property dedicated specifically for living or dwelling for 
                individuals or households; it may include standalone single-family dwellings to large, 
                multi-unit apartment buildings.
                """
            ),
            dcc.Graph(id='injected', figure=rent_indicators, config={'displayModeBar': False}),
            html.P(
                f"""
                Indicators above demonstrate the Average monthly rent per square meter in the chosen 
                postal area compared to average monthly rent per square meter in Helsinki.
                Average monthly rent per square meter in {neighborhood} is {price_per_square:.2f}€. 
                This means that the average monthly rent of a 30m² apartment will be approximately
                {(price_per_square * 35):.2f}€, 60m² apartment will cost {(price_per_square * 65):.2f}€ 
                and 90m² apartment will cost {(price_per_square * 95):.2f}€. If there is not enough data on the
                neighborhood all values will be 0. Average square meters of the apartment can be used to compare
                the average size of the apartments in {neighborhood} to the average size of apartment 
                is Helsinki metropolitan region.
                """
            ),
            dcc.Graph(id='injected2', figure=scatter_chart_rent, config={'displayModeBar': False}),
            html.P(
                """
                Scatterplots above illustrates the relationships between apartment square meters and monthly
                rent in Helsinki Metropolitan area. The graph helps us understand how the change in apartment
                square meters affects the monthly rent.
                """
            ),
        ]

        return children

    # Tab 2 Section 1 Owned Dwellings
    @app.callback(
        Output('id_re_owning', 'children'),
        Input('choropleth-map', 'clickData'))
    def display_click_data(click_data):
        """
        Generates the graphs for owned dwellings section.
        ---
        Args: 
            click_data (dict): dictionary returned by dcc.Graph component triggered by user-interaction.

        Returns: 
            children (list): List of html components to be displayed.
        """
        # Get the postal code based on clicked area
        postal_code = get_postal_code(click_data)

        selling = real_estate[real_estate['deal_type'] == 'sell']
        selling['price_per_square'] = (selling['price'] / selling['area'])

        # get df row based on postal number
        if postal_code in selling.index:
            df = selling.loc[postal_code]
        else:
            df = pd.DataFrame(0.0, columns=selling.columns, index=selling.index)
            
        try:
            neighborhood = df['neighborhood'].values[0]

        except AttributeError:
            neighborhood = df['neighborhood']

        finally:
            neighborhood = ""

        price_per_square = df['price_per_square'].mean()
        average_area = df['area'].mean()
        hels_avg_price_per_square = selling['price_per_square'].mean()
        hels_avg_re_area = selling['area'].mean()

        # Create graph object
        sell_indicators = go.Figure()

        sell_indicators.add_trace(go.Indicator(
            mode="number",
            value=price_per_square,
            number={'prefix': "€", "font": {"size": 40}},
            title={"text": f"Price per m² in {neighborhood}<br><span style='font-size:0.8em;color:gray'>" +
                           "Average price per square meter</span><br>"},
            domain={'x': [0, 0.5], 'y': [0.5, 1]}
            )
        )

        sell_indicators.add_trace(go.Indicator(
            mode="number",
            value=hels_avg_price_per_square,
            number={'prefix': "€", "font": {"size": 40}},
            title={"text": "Average price in Helsinki<br><span style='font-size:0.8em;color:gray'>" +
                           "Average price per square meter for Helsinki </span><br>"},
            domain={'x': [0.5, 1], 'y': [0.5, 1]},
            )
        )

        sell_indicators.add_trace(go.Indicator(
            mode="number",
            value=hels_avg_re_area,
            number={'suffix': " m²", "font": {"size": 40}},
            title={"text": "Average Area in Helsinki<br><span style='font-size:0.8em;color:gray'>" +
                           "All apartments average.</span><br>"},
            domain={'x': [0.5, 1], 'y': [0, .5]},
            )
        )

        sell_indicators.add_trace(go.Indicator(
            mode="number",
            value=average_area,
            number={'suffix': " m²", "font": {"size": 40}},
            title={"text": f"Average area in {neighborhood}<br><span style='font-size:0.8em;color:gray'>" +
                           "All apartments average.</span><br>"},
            domain={'x': [0, 0.5], 'y': [0, 0.5]},
            )
        )

        sell_indicators.update_layout(
            paper_bgcolor='#1E1E1E',
            plot_bgcolor='#1E1E1E',
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            autosize=True,
            font=dict(color="white")
            )
        
        selling_df = real_estate[real_estate['deal_type'] == 'sell']
        selling_df = selling_df[selling_df['price'] < 2000000]
        selling_df = selling_df[selling_df['area'] < 310]

        x = selling_df['area']
        y = selling_df['price']

        scatter_chart_sell = go.Figure(
            data=go.Scattergl(
                x=x,
                y=y,
                mode='markers',
                hovertemplate='<b>Price</b>: €%{y:.2f}' +
                '<br><b>Area</b>: %{x}m²<br>',
                marker=dict(
                    size=8,
                    color=selling_df['rooms'],
                    colorscale='tealgrn',
                    showscale=True,
                )
            )
        )

        scatter_chart_sell.update_layout(
            showlegend=False,
            paper_bgcolor='#1E1E1E',
            plot_bgcolor='#1E1E1E',
            margin={"r": 50, "t": 50, "l": 50, "b": 50},
            autosize=True
        )
        scatter_chart_sell.update_traces(marker=dict(line=dict(color='#1E1E1E', width=3)))
        scatter_chart_sell.update_xaxes(color='#fff', gridcolor='#D3D3D3')
        scatter_chart_sell.update_yaxes(color='#fff', gridcolor='#D3D3D3')
        
        children = [
            html.H5("Own Apartments"),
            html.P(
                """
                Own apartment refers to homes that are inhabited by the owners. Residential property is property zoned
                specifically for living or dwelling for individuals or households; it may include standalone 
                single-family dwellings to large, multi-unit apartment buildings.
                """
            ),
            dcc.Graph(
                id='injected',
                figure=sell_indicators,
                config={'displayModeBar': False}
            ),
            html.P(
                f"""
                Indicators above demonstrate the Average buying price per square meter in {neighborhood} neighborhood
                compared to the average price per square meter in Helsinki metropolitan region. 
                Average price per square meter in {neighborhood} is {price_per_square:.2f}€. 
                This means that the average price of a 30m² apartment will be approximately 
                {(price_per_square * 35):.2f}€, 60m² apartment will cost {(price_per_square * 65):.2f}€ and 90m² 
                apartment will cost {(price_per_square * 95):.2f}€. If there is not enough data on the neighborhood 
                all values will be 0. Average square meters of the apartment can be used to compare the 
                average size of the apartments in {neighborhood} to the average size of apartment is 
                Helsinki metropolitan region. Note that In Finland, when you "buy an apartment" what 
                you are actually buying are shares in a housing company (asunto-osakeyhtiö).
                The amount of shares per apartment is proportional to the size of the apartment.
                """
            ),
            dcc.Graph(
                id='injected2',
                figure=scatter_chart_sell,
                config={'displayModeBar': False}
            ),
            html.P(
                """
                Scatterplots above illustrates the relationships between apartment square meters and apartment 
                price in Helsinki Metropolitan area. The graph helps us understand how the change in apartment 
                square meters affects the buying/selling price of the apartments.
                """
            ),            
        ]

        return children

    # Tab 2 Section 1 Sauna Index
    @app.callback(
        Output('id_re_sauna', 'children'),
        Input('choropleth-map', 'clickData'))
    def display_click_data(click_data):
        """
        Generates the graphs for sauna index section.
        ---
        Args: 
            click_data (dict): dictionary returned by dcc.Graph component triggered by user-interaction.

        Returns: 
            children (list): List of html components to be displayed.
        """
        # Section title
        section_title = "Sauna Index"

        # Get the postal code based on clicked area
        postal_code = get_postal_code(click_data)

        # get df row based on postal number
        if postal_code in real_estate.index:
            df = real_estate.loc[postal_code]
        else:
            df = pd.DataFrame(0.0, columns=real_estate.columns, index=real_estate.index)
            
        try:
            neighborhood = real_estate['neighborhood'].values[0]

        except AttributeError:
            neighborhood = real_estate['neighborhood']

        finally:
            neighborhood = "" 

        # Data privacy check
        if privacy_check(postal_code):
            return privacy_notice(section_title, neighborhood)

        # Get number of saunas
        saunas = df[df['sauna'] == True]
        number_of_saunas = len(saunas)

        # Create Graph Object
        sauna = go.Figure()

        sauna.add_trace(go.Indicator(
            mode="number",
            value=number_of_saunas,
            number={'prefix': "#"},
            title={"text": f"Sauna Index{neighborhood}<br><span style='font-size:0.8em;color:gray'>" +
                           "Number of known saunas in the area</span><br>"},
            )
        )
        
        sauna.update_layout(
            paper_bgcolor='#1E1E1E',
            plot_bgcolor='#1E1E1E',
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            autosize=True,
            font=dict(color="white")
        )

        children = [
            html.H5(section_title),
            html.P(
                """
                Dashmap Sauna index is a cutting edge urban metrics that highlights the number of available saunas 
                in the postal code area. These are the saunas present in the apartments that are 
                currently on the market. If leveraged properly this revolutionary metrics can boost your 
                productivity and reduce stress.
                """
            ),
            dcc.Graph(
                id='injected',
                figure=sauna,
                config={'displayModeBar': False}
            ),
            html.P(
                """
                *This is an experimental metric. The actual number of saunas is dramatically higher!
                However, due to limited availability of data a precise estimate cannot be made.
                """
            ),
        ]

        return children