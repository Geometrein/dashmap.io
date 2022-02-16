from dash import html
from dash import dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from ..util.helpers import privacy_check, privacy_notice, get_postal_code

colors = [
    '#4182C8', '#2E94B2',
    '#39A791', '#6FB26C',
    '#C0C15C', '#F9BD24',
    '#F3903F', '#EC6546',
    '#7D4C94', '#5B61AE'
]

def init_services_callbacks(app, datum):
    """
    """
    # Tab 3 Section 1 Workplaces Pie chart CallBack
    @app.callback(
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
    @app.callback(
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