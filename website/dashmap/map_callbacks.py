import pandas as pd
# Dash
import dash
from dash import html
from dash import dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
# Plotly Graph Objects
from .map_graphs import *

from .callbacks.util.helpers import *
from .callbacks.accordions.init_accordions import init_all_accordions

from .callbacks.tab_census.census_callbacks import init_census_callbacks
pd.options.mode.chained_assignment = None

# Load datasets
datum, real_estate, bus_stops = load_datum()


# CallBacks
def init_callbacks(dash_app: dash.callback_context) -> None:
    """
    Initialize Dash callbacks.
    ---
    Args: Dash app object

    Returns: None
    """
    
    init_modal_popup(dash_app)
    init_all_accordions(dash_app)

    init_census_callbacks(dash_app, datum)
 
    # Tab 2 Section 1 Rental Dwellings
    @dash_app.callback(
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

        # get df row based on postal number
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
    @dash_app.callback(
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
    @dash_app.callback(
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

    # Tab 3 Section 1 Workplaces Pie chart CallBack
    @dash_app.callback(
        Output('id_services_industries', 'children'),
        Input('choropleth-map', 'clickData'))
    def display_click_data(click_data):
        """
        Generates the graphs for Industries section.
        ---
        Args: 
            click_data (dict): dictionary returned by dcc.Graph component triggered by user-interaction.

        Returns: 
            children (list): List of html components to be displayed.
        """
        section_title = "Economic Structure"

        # Get the postal code based on clicked area
        postal_code = get_postal_code(click_data)

        # Get df row based on postal number
        result = datum.loc[postal_code]
        neighborhood = result['neighborhood']

        # Data privacy check
        if privacy_check(postal_code):
            return privacy_notice(section_title, neighborhood)

        work_services = result["Services, 2018 (TP)"]
        work_other = int(result["Primary production, 2018 (TP)"]) + int(result["Processing, 2018 (TP)"])

        workplaces_values = [work_other, work_services]
        workplaces_values = [int(i) for i in workplaces_values]

        workplaces_labels = ["Processing & Production", "Services"]

        # Create pie chart figure
        workplaces_pie_chart = go.Figure(
            data=[
                go.Pie(
                    labels=workplaces_labels, 
                    values=workplaces_values, 
                    hole=0.7
                )
            ]
        )

        workplaces_pie_chart.update_layout(
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="middle",
                y=-0.1,
                xanchor="center",
                x=.5
            ),
            font=dict(
                size=14,
                color="#fff"
            ),
            paper_bgcolor='#1E1E1E', 
            plot_bgcolor='#1E1E1E', 
            margin={"r": 30, "t": 30, "l": 30, "b": 30},
            autosize=True
        )

        workplaces_pie_chart.update_traces(
            hoverinfo='label+percent',
            marker=dict(
                colors=colors,
                line=dict(
                    color='#1E1E1E',
                    width=2
                )
            )
        )
        intro = f"""
        Most developed countries have service oriented economy and Finland is no exception. 
        In service oriented economies economic activity is
        a collaborative process wherein all parties co-create value through reciprocal service provision.
        Whereas in goods dominated economies tangible products are the primary focus of economic exchange.
        Services are the primary economic activity in {neighborhood} neighborhood.
        """
        processing_production = """
        Agriculture, forestry and fishing.
        Processing includes mining, manufacturing, 
        electricity, gas, steam and air conditioning supply
        water supply; sewerage, waste management and remediation activities,
        construction
        """
        services = """
        Services include wholesale and retail trade, transportation and storage,
        accommodation and food service activities, information and communication,
        financial and insurance activities, real estate activities,
        professional, scientific and technical activities,
        administrative and support service activities,
        public administration and defence, education,
        human health and social work activities,
        arts, entertainment and recreation, other service activities,
        activities of households as employers,
        activities of extraterritorial organizations and bodies.
        """
        children = [
            html.H4(section_title),
            html.P(intro),
            dcc.Graph(id='injected2', figure=workplaces_pie_chart, config={'displayModeBar': False}),
            html.Br(),
            html.H5("Services"),
            html.P(services),
            html.Br(),           
            html.H5("Processing & Production"),
            html.P(processing_production),
        ]

        return children

    # Tab 3 Section 2 Workplaces Pie chart CallBack
    @dash_app.callback(
        Output('id_workplaces', 'children'),
        Input('choropleth-map', 'clickData'))
    def display_click_data(click_data):
        """
        Generates the graphs for Workplaces section.
        ---
        Args: 
            click_data (dict): dictionary returned by dcc.Graph component triggered by user-interaction.

        Returns: 
            children (list): List of html components to be displayed.
        """
        section_title = "Workplaces"

        # Get the postal code based on clicked area
        postal_code = get_postal_code(click_data)

        # Get df row based on postal number
        result = datum.loc[postal_code]
        neighborhood = result['neighborhood']

        # Data privacy check
        if privacy_check(postal_code):
            return privacy_notice(section_title, neighborhood)

        work_total = result["Workplaces, 2018 (TP)"]

        # Create Graph Object
        workplaces = go.Figure()

        workplaces.add_trace(go.Indicator(
            mode="number",
            value=work_total,
            title={"text": f"Total Workplaces<br><span style='font-size:0.8em;color:gray'>" +
                             "Number of Workplaces in the area</span><br>"},
            )
        )
        
        workplaces.update_layout(
            paper_bgcolor='#1E1E1E',
            plot_bgcolor='#1E1E1E',
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            autosize=True,
            font=dict(color="white")
        )
        # Set column indexes
        index_start = 77
        index_end = 99

        # Filter the dataframe based on column indexes
        industry_bins = result.tolist()[index_start:index_end]
        industry_bins = [int(i) for i in industry_bins]

        # Create Histogram Bins
        x = result.index.tolist()[index_start:index_end]
        x = [i.split(' ')[0] for i in x]

        # Create pie chart figure object
        workplace_hist = go.Figure(
            data=[
                go.Bar(
                    name=neighborhood,
                    x=x, 
                    y=industry_bins,
                    marker_color='#4182C8',
                )
                
            ]
        )

        workplace_hist.update_layout(
            font=dict(
                size=14,
                color="#fff"
            ),
            legend=dict(
                orientation="v",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5,
            ),
            paper_bgcolor='#1E1E1E', 
            plot_bgcolor='#1E1E1E', 
            margin={"r": 30, "t": 30, "l": 30, "b": 30},
            autosize=True
        )
        workplace_hist.update_traces(
            hoverinfo='text',

        )

        workplace_legend = result.index.tolist()[index_start:index_end]
        workplace_legend = [i.replace('2018 (TP)', '') for i in workplace_legend]
        workplace_legend = [i.split(';')[0] for i in workplace_legend]

        text = f"""
        The graph below illustrates the number of workplaces in the {neighborhood} area by the industry sector.
        """
        by_industry = "Workplaces by Industry"

        children = [
            html.H4(section_title),
            dcc.Graph(id='injected1', figure=workplaces, config={'displayModeBar': False}),
            html.H4(by_industry),
            html.Hr(),
            html.P(text),
            dcc.Graph(id='injected2', figure=workplace_hist, config={'displayModeBar': False}),
            html.Ul(id='legend-list', children=[html.Li(i) for i in workplace_legend])
        ]

        return children

    # Tab 4 Section 1 mobility CallBack
    @dash_app.callback(
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
    @dash_app.callback(
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

    # Tab 5 Section 1 air temp CallBack
    @dash_app.callback(
        Output('id_air_temperature', 'children'),
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
    @dash_app.callback(
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
