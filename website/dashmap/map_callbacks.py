import pandas as pd
# Dash
import dash
from dash import html
from dash import dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
# Plotly Graph Objects
from .map_graphs import *

pd.options.mode.chained_assignment = None

# Load datasets
datum, real_estate, bus_stops = load_datum()


def get_postal_code(click_data: dict) -> str:
    """
    Helper function for the callbacks
    Gets postal code from map click_data.
    ---
    Args: 
        click_data (dict): user click information

    Returns: 
        postal_code (str): Area postal code. '00180' by default.
    """

    # try to find the area by postcode
    try: 
        postal_code = str(click_data["points"][0]['location'])
    except:
        postal_code = '00180'  # Kamppi Postal code

    return postal_code


def privacy_check(postal_code: str) -> bool:
    """
    Helper function for the callbacks.
    Checks if postal code is private.
    ---
    Args: 
        postal_code (str): Area postal code.

    Returns: 
        True (bool): When postal code is in the private_list
        False (bool): When postal code is not found in the private_list
    """
    # List of private area postcodes
    private_list = ['00230', '02290', '01770']

    if postal_code in private_list:
        return True
    else:
        return False


def privacy_notice(section_title: str, neighborhood: str) -> list:
    """
    Helper function for the callbacks.
    ---
    Args: 
        section_title (str): Title of a sections
        neighborhood (str): name of the neighborhood 

    Returns: 
        children (list): List of html components to be displayed.
    """

    privacy_notice_text = f"""
            The statistical data about postal areas where less than 30 citizens live is 
            private due to possible privacy violations. Additionally the data representing 
            such a small population will not yield statistically significant insights.
            For these reason the data available for {neighborhood} neighborhood will not be displayed.
            """

    children = [
        html.H5(section_title),
        html.P(privacy_notice_text),
        html.P("Check out the other postal areas!")
    ]

    return children


# CallBacks
def init_callbacks(dash_app: dash.callback_context) -> None:
    """
    Initialize Dash callbacks.
    ---
    Args: Dash app object

    Returns: None
    """
    # Help Modal
    @dash_app.callback(
        Output("help-modal-centered", "is_open"),
        [Input("help-open-centered", "n_clicks"), Input("help-close-centered", "n_clicks")],
        [State("help-modal-centered", "is_open")],
    )
    def toggle_modal(n1: str, n2: str, is_open: bool):
        """
        Toggle modal pop-ups.
        ---
        Args:
            n1 (str): id of the trigger button
            n2 (str): id of the trigger button
            is_open (bool): Current state of the modal. True for Open, False otherwise.

        Returns:
            is_open (bool): True for Open, False otherwise. Default value is False.
        """
        if n1 or n2:
            return not is_open
        return is_open

    # Tab Census Section individuals Accordion CallBacks
    @dash_app.callback(
        [Output(f"tab-1-collapse-{i}", "is_open") for i in range(1, 6)],
        [Input(f"tab-1-group-{i}-toggle", "n_clicks") for i in range(1, 6)],
        [State(f"tab-1-collapse-{i}", "is_open") for i in range(1, 6)],
    )
    def toggle_accordion(n1, n2, n3, n4, n5, is_open1, is_open2, is_open3, is_open4, is_open5):
        """
        Toggle accordion collapse & expand.
        ---
        Args: 
            n1 -> n5 (str): id of the trigger button  
            is_open1 -> is_open5 (bool): Current state of the accordion. True for Open, False otherwise.

        Returns: 
            (bool): Boolean values for each accordion tab. True for Open, False otherwise. Default value is False.
        """

        ctx = dash.callback_context

        if not ctx.triggered:
            return False, False, False, False, False
        else:
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "tab-1-group-1-toggle" and n1:
            return not is_open1, False, False, False, False
        elif button_id == "tab-1-group-2-toggle" and n2:
            return False, not is_open2, False, False, False
        elif button_id == "tab-1-group-3-toggle" and n3:
            return False, False, not is_open3, False, False
        elif button_id == "tab-1-group-4-toggle" and n4:
            return False, False, False, not is_open4, False
        elif button_id == "tab-1-group-5-toggle" and n5:
            return False, False, False, False, not is_open5

        return False, False, False, False, False

    # Tab Census Section Households Accordion CallBacks
    @dash_app.callback(
        [Output(f"tab-1-2-collapse-{i}", "is_open") for i in range(1, 5)],
        [Input(f"tab-1-2-group-{i}-toggle", "n_clicks") for i in range(1, 5)],
        [State(f"tab-1-2-collapse-{i}", "is_open") for i in range(1, 5)],
    )
    def toggle_accordion(n1, n2, n3, n4, is_open1, is_open2, is_open3, is_open4):
        """
        Toggle accordion collapse & expand.
        ---
        Args: 
            n1 -> n4 (str): id of the trigger button  
            is_open1 -> is_open4 (bool): Current state of the accordion. True for Open, False otherwise.

        Returns: 
            (bool): Boolean values for each accordion tab. True for Open, False otherwise. Default value is False.
        """

        ctx = dash.callback_context
        if not ctx.triggered:
            return False, False, False, False
        else:
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "tab-1-2-group-1-toggle" and n1:
            return not is_open1, False, False, False
        elif button_id == "tab-1-2-group-2-toggle" and n2:
            return False, not is_open2, False, False
        elif button_id == "tab-1-2-group-3-toggle" and n3:
            return False, False, not is_open3, False
        elif button_id == "tab-1-2-group-4-toggle" and n4:
            return False, False, False, not is_open4

        return False, False, False, False

    # Tab Real Estate Accordion CallBacks
    @dash_app.callback(
        [Output(f"tab-2-collapse-{i}", "is_open") for i in range(2, 5)],
        [Input(f"tab-2-group-{i}-toggle", "n_clicks") for i in range(2, 5)],
        [State(f"tab-2-collapse-{i}", "is_open") for i in range(2, 5)],
    )
    def toggle_accordion(n2, n3, n4, is_open2, is_open3, is_open4):
        """
        Toggle accordion collapse & expand.
        ---
        Args: 
            n1 -> n4 (str): id of the trigger button  
            is_open1 -> is_open4 (bool): Current state of the accordion. True for Open, False otherwise.

        Returns: 
            (bool): Boolean values for each accordion tab. True for Open, False otherwise. Default value is False.
        """
        ctx = dash.callback_context

        if not ctx.triggered:
            return False, False, False
        else:
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "tab-2-group-2-toggle" and n2:
            return not is_open2, False, False
        elif button_id == "tab-2-group-3-toggle" and n3:
            return False, not is_open3, False
        elif button_id == "tab-2-group-4-toggle" and n4:
            return False, False, not is_open4

        return False, False, False

    # Tab Services Accordion CallBacks
    @dash_app.callback(
        [Output(f"tab-3-collapse-{i}", "is_open") for i in range(1, 3)],
        [Input(f"tab-3-group-{i}-toggle", "n_clicks") for i in range(1, 3)],
        [State(f"tab-3-collapse-{i}", "is_open") for i in range(1, 3)],
    )
    def toggle_accordion(n1, n2, is_open1, is_open2):
        """
        Toggle accordion collapse & expand.
        ---
        Args: 
            n1 -> n2 (str): id of the trigger button  
            is_open1 -> is_open2 (bool): Current state of the accordion. True for Open, False otherwise.

        Returns: 
            (bool): Boolean values for each accordion tab. True for Open, False otherwise. Default value is False.
        """

        ctx = dash.callback_context
        if not ctx.triggered:
            return False, False
        else:
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "tab-3-group-1-toggle" and n1:
            return not is_open1, False
        elif button_id == "tab-3-group-2-toggle" and n2:
            return False, not is_open2

        return False, False

    # Tab Mobility Section  Accordion CallBacks
    @dash_app.callback(
        [Output(f"tab-4-collapse-{i}", "is_open") for i in range(1, 3)],
        [Input(f"tab-4-group-{i}-toggle", "n_clicks") for i in range(1, 3)],
        [State(f"tab-4-collapse-{i}", "is_open") for i in range(1, 3)],
    )
    def toggle_accordion(n1, n2, is_open1, is_open2):
        """
        Toggle accordion collapse & expand.
        ---
        Args: 
            n1 -> n4 (str): id of the trigger button  
            is_open1 -> is_open4 (bool): Current state of the accordion. True for Open, False otherwise.

        Returns: 
            (bool): Boolean values for each accordion tab. True for Open, False otherwise. Default value is False.
        """

        ctx = dash.callback_context

        if not ctx.triggered:
            return False, False
        else:
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "tab-4-group-1-toggle" and n1:
            return not is_open1, False
        elif button_id == "tab-4-group-2-toggle" and n2:
            return False, not is_open2

        return False, False

    # Tab Environment Section Accordion CallBacks
    @dash_app.callback(
        [Output(f"tab-5-collapse-{i}", "is_open") for i in range(1, 4)],
        [Input(f"tab-5-group-{i}-toggle", "n_clicks") for i in range(1, 4)],
        [State(f"tab-5-collapse-{i}", "is_open") for i in range(1, 4)],
    )
    def toggle_accordion(n1, n2, n3, is_open1, is_open2, is_open3):
        """
        Toggle accordion collapse & expand.
        ---
        Args: 
            n1 -> n2 (str): id of the trigger button  
            is_open1 -> is_open2 (bool): Current state of the accordion. True for Open, False otherwise.

        Returns: 
            (bool): Boolean values for each accordion tab. True for Open, False otherwise. Default value is False.
        """

        ctx = dash.callback_context
        if not ctx.triggered:
            return False, False, False
        else:
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "tab-5-group-1-toggle" and n1:
            return not is_open1, False, False
        elif button_id == "tab-5-group-2-toggle" and n2:
            return False, not is_open2, False
        elif button_id == "tab-5-group-3-toggle" and n3:
            return False, False, not is_open3

        return False, False, False

    # Tab 1 Section 1 Age Distribution CallBack
    @dash_app.callback(
        Output('id_age_dist_hist', 'children'),
        Input('choropleth-map', 'clickData'))
    def display_click_data(click_data):
        """
        Generates the graphs for Age Distribution section.
        ---
        Args: 
            click_data (dict): dictionary returned by dcc.Graph component triggered by user-interaction.

        Returns: 
            children (list): List of html components to be displayed.
        """
        section_title = "Age Distribution"

        # Get the postal code based on clicked area
        postal_code = get_postal_code(click_data)

        # get df row based on postal number
        result = datum.loc[postal_code]
        neighborhood = result['neighborhood']

        # Data privacy check
        if privacy_check(postal_code):
            return privacy_notice(section_title, neighborhood)

        index_start = 7
        index_end = 27

        age_bins = result.tolist()[index_start:index_end]

        # Get Helsinki Averages
        mean_age = result['Average age of inhabitants, 2019 (HE)']
        age_bins = [int(i) for i in age_bins]

        x = result.index.tolist()[index_start:index_end]
        x = [i.split(' ')[0] for i in x]

        columns_list = datum.columns[7:27]
        y2 = [datum[column].astype(float).mean() for column in columns_list]

        # Create pie chart figure object
        age_dist_hist = go.Figure(
            data=[
                go.Bar(
                    name=neighborhood,
                    x=x, 
                    y=age_bins,
                    marker_color='#4182C8',
                )
                
            ]
        )

        # Average age distribution in Helsinki
        age_dist_hist.add_trace(
            go.Bar(
                name='Helsinki Average',
                x=x,
                y=y2,
                marker_color='#F3903F',
                visible='legendonly',
            )
        )

        age_dist_hist.update_layout(
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
            paper_bgcolor='#1E1E1E', 
            plot_bgcolor='#1E1E1E', 
            margin={"r": 30, "t": 30, "l": 30, "b": 30},
            autosize=True
        )
        age_dist_hist.update_traces(
            hoverinfo='text',


        )
        
        text = f"""
            Age distribution, also called Age Composition, is the proportionate numbers 
            of persons in successive age categories in a given population.
            The graph above illustrates the age distribution in {neighborhood} neighborhood. 
            The average age of the inhabitant in {neighborhood} area is {mean_age}.
            Age distributions might differ dramatically among different postal areas.
            Factors such as fertility, popularity of the area among certain age groups can affect the 
            age composition of the area. If the bins on the right side of the histogram are higher it means 
            that the population is shrinking and aging. If the bins on the left side are higher it means that 
            the population is young and growing. 
            """

        children = [
            html.H5(section_title),
            dcc.Graph(id='injected', figure=age_dist_hist, config={'displayModeBar': False}),
            html.P(text)
        ]

        return children

    # Tab 1 Section 1 Gender Distribution CallBack
    @dash_app.callback(
        Output('id_gender_pie_chart', 'children'),
        Input('choropleth-map', 'clickData'))
    def display_click_data(click_data):
        """
        Generates the graphs for Gender Distribution section.
        ---
        Args: 
            click_data (dict): dictionary returned by dcc.Graph component triggered by user-interaction.

        Returns: 
            children (list): List of html components to be displayed.
        """
        # Title of this section
        section_title = "Gender Composition"

        # Get the postal code based on clicked area
        postal_code = get_postal_code(click_data)

        # Get df row based on postal number
        result = datum.loc[postal_code]
        neighborhood = result['neighborhood']

        # Data privacy check
        if privacy_check(postal_code):
            return privacy_notice(section_title, neighborhood)

        # Get number of males and females in a district
        males = result['Males, 2019 (HE)']
        females = result['Females, 2019 (HE)']

        # Get gender pie chart values and labels
        gender_pie_chart_values = [males, females]
        gender_pie_chart_labels = ["Males", "Females"]

        # Create pie chart figure object
        gender_pie_chart = go.Figure(
            data=[
                go.Pie(
                    labels=gender_pie_chart_labels, 
                    values=gender_pie_chart_values, 
                    hole=.7
                )
            ]
        )

        gender_pie_chart.update_layout(
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=.5,
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

        gender_pie_chart.update_traces(
            hoverinfo='label+percent+value',
            marker=dict(
                colors=['#4182C8', '#2E94B2'],
                line=dict(
                    color='#1E1E1E',
                    width=2
                )
            )
        )

        # Default text body
        text = f"""
            The graph above illustrates the distribution of males and females in {neighborhood} neighborhood.  
            Gender distribution has a measurable and proven impact on a wide range of societal, demographic, and the
            economic processes within the city. This distribution is not constant. It is affected by biological,
            social, cultural, and economic forces.
            """

        # Conditionally formatting text based on data
        if int(gender_pie_chart_values[0]) > int(gender_pie_chart_values[1]):
            text += f"men outnumber women in {neighborhood} neighborhood."
        elif int(gender_pie_chart_values[0]) < int(gender_pie_chart_values[1]):
            text += f"women outnumber men in {neighborhood} neighborhood."
        else:
            text += f" the distribution of men and women in the {neighborhood} neighborhood is roughly equal."

        children = [
            html.H5(section_title),
            dcc.Graph(id='injected', figure=gender_pie_chart, config={'displayModeBar': False},),
            html.P(text),
        ]

        return children

    # Tab 1 Section 1 Education Pie chart CallBack
    @dash_app.callback(
        Output('id_education_pie_chart', 'children'),
        Input('choropleth-map', 'clickData'))
    def display_click_data(click_data):
        """
        Generates the graphs for Education section.
        ---
        Args: 
            click_data (dict): dictionary returned by dcc.Graph component triggered by user-interaction.

        Returns: 
            children (list): List of html components to be displayed.
        """
        section_title = "Education"

        # Get the postal code based on clicked area
        postal_code = get_postal_code(click_data)

        # Get df row based on postal number
        result = datum.loc[postal_code]
        neighborhood = result['neighborhood']

        # Data privacy check
        if privacy_check(postal_code):
            return privacy_notice(section_title, neighborhood)

        index_start = 28
        index_end = 34

        education_values = result.tolist()[index_start:index_end]
        education_values.pop(1)  # remove "With Education" column
        education_values = [int(i) for i in education_values]

        education_labels = result.index.tolist()[index_start:index_end]
        education_labels.pop(1)
        education_labels = [i.split(',')[0] for i in education_labels]

        # Create pie chart figure
        education_pie_chart = go.Figure(
            data=[
                go.Pie(
                    labels=education_labels, 
                    values=education_values, 
                    hole=0
                )
            ]
        )

        education_pie_chart.update_layout(
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="middle",
                y=-.5,
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

        education_pie_chart.update_traces(
            hoverinfo='label+percent+value',
            marker=dict(
                colors=colors,
                line=dict(
                    color='#1E1E1E',
                    width=2
                )
            )
        )

        text = f"""
            The graph above illustrates the distribution of individuals by their 
            level of education in {neighborhood} neighborhood.
            """

        children = [
            html.H5(section_title),
            dcc.Graph(id='injected', figure=education_pie_chart, config={'displayModeBar': False},),
            html.P(text),
        ]

        return children

    # Tab 1 Section 1 Income CallBack
    @dash_app.callback(
        Output('id_income_pie_chart', 'children'),
        Input('choropleth-map', 'clickData'))
    def display_click_data(click_data):
        """
        Generates the graphs for Income section.
        ---
        Args: 
            click_data (dict): dictionary returned by dcc.Graph component triggered by user-interaction.

        Returns: 
            children (list): List of html components to be displayed.
        """
        section_title = "Individual Income Levels"
        section_description = """
            Disposable income is the income remaining after deduction of taxes and social security charges.
            """

        # Get the postal code based on clicked area
        postal_code = get_postal_code(click_data)

        # get df row based on postal number
        result = datum.loc[postal_code]
        neighborhood = result['neighborhood']

        # Data privacy check
        if privacy_check(postal_code):
            return privacy_notice(section_title, neighborhood)
        
        mean_income_helsinki = datum['Average income of inhabitants, 2019 (HR)'].astype(int).mean()
        median_income_helsinki = datum['Average income of inhabitants, 2019 (HR)'].astype(int).median()

        # Name of the column contains a type Inhabintants
        lower_class = result['Inhabintants belonging to the lowest income category, 2019 (HR)']
        middle_class = result['Inhabitants belonging to the middle income category, 2019 (HR)']
        upper_class = result['Inhabintants belonging to the highest income category, 2019 (HR)']
        mean_income = result['Average income of inhabitants, 2019 (HR)']
        median_income = result['Median income of inhabitants, 2019 (HR)']

        # Get gender columns
        income_level_values = [lower_class, middle_class, upper_class]
        income_level_labels = ["Lower Class", "Middle Class", "Upper Class"]

        # Create pie chart figure
        income_pie_chart = go.Figure(
            data=[
                go.Pie(
                    labels=income_level_labels, 
                    values=income_level_values, 
                    hole=.7
                )
            ]
        )

        income_pie_chart.update_layout(
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-.15,
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

        income_pie_chart.update_traces(
            hoverinfo='label+percent+value',
            marker=dict(
                colors=colors,
                line=dict(
                    color='#1E1E1E',
                    width=2
                )
            )
        )

        # Create Graph Object
        income_indicators = go.Figure()

        income_indicators.add_trace(
            go.Indicator(
                mode="number",
                value=int(mean_income),
                number={'prefix': "€", "font": {"size": 40}},
                title={"text": "Average Income<br><span style='font-size:0.8em;color:gray'>" +
                               "Avg. individual income in postal area</span><br>"},
                domain={'x': [0, 0.5], 'y': [.5, 1]},
            )
        )

        income_indicators.add_trace(
            go.Indicator(
                mode="number",
                value=int(median_income),
                number={'prefix': "€", "font": {"size": 40}},
                title={"text": "Median Income<br><span style='font-size:0.8em;color:gray'>" +
                               "Median individual income in whole Helsinki</span><br>"},
                domain={'x': [0, 0.5], 'y': [0, .5]}
            )
        )

        income_indicators.add_trace(
            go.Indicator(
                mode="number",
                value=int(mean_income_helsinki),
                number={'prefix': "€", "font": {"size": 40}},
                title={"text": "Average Income Helsinki<br><span style='font-size:0.8em;color:gray'>" +
                               "Avg. individual income in postal area</span><br>"},
                domain={'x': [0.5, 1], 'y': [0.5, 1]}
            )
        )
        
        income_indicators.add_trace(
            go.Indicator(
                mode="number",
                value=int(median_income_helsinki),
                number={'prefix': "€", "font": {"size": 40}},
                title={"text": "Median Income in Helsinki<br><span style='font-size:0.8em;color:gray'>" +
                               "Median individual income in whole Helsinki</span><br>"},
                domain={'x': [0.5, 1], 'y': [0, .5]}
            )
        )
        # Update layout 
        income_indicators.update_layout(
                paper_bgcolor='#1E1E1E',
                plot_bgcolor='#1E1E1E',
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                autosize=True,
                font=dict(color="white")
        )

        # Default texts
        text_1 = f"""
            The graph above illustrates the class distribution of individuals in {neighborhood} neighborhood.
            This distribution is not constant. It is affected by a multitude social and economic forces.
            """
        text_2 = f"""
        The average income of an individual in {neighborhood} is {mean_income}€ per year.
        While the median income is {median_income}€ per year.
        """

        children = [
            html.H5(section_title),
            html.P(section_description),
            dcc.Graph(id='injected-indicators', figure=income_indicators, config={'displayModeBar': False},),
            html.P(text_2),
            dcc.Graph(id='injected', figure=income_pie_chart, config={'displayModeBar': False},),
            html.P(text_1),
        ]

        return children

    # Tab 1 Section 1 Employment CallBack
    @dash_app.callback(
        Output('id_employment_pie_chart', 'children'),
        Input('choropleth-map', 'clickData'))
    def display_click_data(click_data):
        """
        Generates the graphs for Employment section.
        ---
        Args: 
            click_data (dict): dictionary returned by dcc.Graph component triggered by user-interaction.

        Returns: 
            children (list): List of html components to be displayed.
        """

        section_title = "Employment Status"

        # Get the postal code based on clicked area
        postal_code = get_postal_code(click_data)

        # get df row based on postal number
        result = datum.loc[postal_code]
        neighborhood = result['neighborhood']

        # Data privacy check
        if privacy_check(postal_code):
            return privacy_notice(section_title, neighborhood)
        
        # get relevant data
        employed = result['Employed, 2018 (PT)']
        unemployed = result['Unemployed, 2018 (PT)']
        students = result['Students, 2018 (PT)']
        pensioners = result['Pensioners, 2018 (PT)']
        other = result['Others, 2018 (PT)']

        # Get gender columns
        employment_level_values = [employed, unemployed, pensioners, students, other]
        employment_level_labels = ["Employed", "Unemployed", "Pensioners", "Students", "Other"]

        # Create pie chart figure
        income_pie_chart = go.Figure(
            data=[
                go.Pie(
                    labels=employment_level_labels,
                    values=employment_level_values,
                    hole=.7
                )
            ]
        )

        income_pie_chart.update_layout(
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-.15,
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

        income_pie_chart.update_traces(
            hoverinfo='label+percent+value',
            marker=dict(
                colors=colors,
                line=dict(
                    color='#1E1E1E',
                    width=2
                )
            )
        )

        text_1 = f"""
            The graph above illustrates the employment status of individuals in {neighborhood} neighborhood.
            This distribution is not constant. It is affected by biological, social, cultural, and economic forces.
            """

        children = [
            html.H5(section_title),
            dcc.Graph(id='injected', figure=income_pie_chart, config={'displayModeBar': False},),
            html.P(text_1),
        ]

        return children

    # Tab 1 Section 2 Household Size
    @dash_app.callback(
        Output('id_household_size', 'children'),
        Input('choropleth-map', 'clickData'))
    def display_click_data(click_data):
        """
        Generates the graphs for Household Size section.
        ---
        Args: 
            click_data (dict): dictionary returned by dcc.Graph component triggered by user-interaction.

        Returns: 
            children (list): List of html components to be displayed.
        """

        section_title = "Household Size"

        # Get the postal code based on clicked area
        postal_code = get_postal_code(click_data)

        # get df row based on postal number
        result = datum.loc[postal_code]
        neighborhood = result['neighborhood']

        # Data privacy check
        if privacy_check(postal_code):
            return privacy_notice(section_title, neighborhood)
        
        helsinki_mean_household_size = datum['Average size of households, 2019 (TE)'].astype(float).mean()
        helsinki_mean_occupancy_rate = datum['Occupancy rate, 2019 (TE)'].astype(float).mean()

        households_total = result['Households, total, 2019 (TE)']
        mean_household_size = result['Average size of households, 2019 (TE)']
        occupancy_rate = result['Occupancy rate, 2019 (TE)']
        
        household_basic_indicators = go.Figure()

        household_basic_indicators.add_trace(go.Indicator(
            mode="number+delta",
            value=int(households_total),
            number={"font": {"size": 40}},
            title={"text": "Total Households<br><span style='font-size:0.8em;color:gray'>" +
                           "In selected postal area</span><br>"},
            domain={'x': [0, 1], 'y': [.5, 1]},
            )
        )

        household_basic_indicators.add_trace(go.Indicator(
            mode="number",
            value=float(mean_household_size),
            number={"font": {"size": 40}},
            title={"text": "Average Household Size<br><span style='font-size:0.8em;color:gray'>" +
                           "Avg. number of people in a household</span><br>"},
            domain={'x': [0, .5], 'y': [0, .5]},
            delta={'reference': helsinki_mean_household_size, 'relative': True, 'position': "top"}
            )
        )

        household_basic_indicators.add_trace(go.Indicator(
            mode="number",
            value=float(occupancy_rate),
            number={'suffix': ' m²', "font": {"size": 40}},
            title={"text": "Occupancy Rate<br><span style='font-size:0.8em;color:gray'>" +
                           "Total floor area / number of inhabitants.</span><br>"},
            domain={'x': [.5, 1], 'y': [0, .5]},
            delta={'reference': helsinki_mean_occupancy_rate, 'relative': True, 'position': "top"}
            )
        )

        household_basic_indicators.update_layout(
                paper_bgcolor='#1E1E1E',
                plot_bgcolor='#1E1E1E',
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                autosize=True,
                font=dict(color="white")
            )

        text_1 = f"""
            The indicators above illustrates the key household size metrics in {neighborhood} neighborhood.
            There are {households_total:.2F} households in {neighborhood} neighborhood.
            The average household size is {mean_household_size} people and Occupancy rate is {occupancy_rate}
            """

        children = [
            html.H5(section_title),
            html.P("""
            Household Size is the number of persons (irrespective of age) living as an economic unit.
            This is very much a function of the age profile of the population.
            Younger populations invariably have a larger average household size than older populations. 
            It is also influenced by the birth rates. The lower the birth rates the smaller the number of 
            people in the household. This is typically an important metrics for understanding the 
            demographic profile of a population.
            """),
            dcc.Graph(id='injected-indicators', figure=household_basic_indicators, config={'displayModeBar': False},),
            html.P(text_1),
        ]

        return children

    # Tab 1 Section 2 Household Structure
    @dash_app.callback(
        Output('id_household_structure', 'children'),
        Input('choropleth-map', 'clickData'))
    def display_click_data(click_data):
        """
        Generates the graphs for Household Structure section.
        ---
        Args: 
            click_data (dict): dictionary returned by dcc.Graph component triggered by user-interaction.

        Returns: 
            children (list): List of html components to be displayed.
        """
        section_title = "Household Structure"
        
        # Get the postal code based on clicked area
        postal_code = get_postal_code(click_data)

        # get df row based on postal number
        result = datum.loc[postal_code]
        neighborhood = result['neighborhood']

        # Data privacy check
        if privacy_check(postal_code):
            return privacy_notice(section_title, neighborhood)

        # mean values
        young_single_mean = datum['Young single persons, 2019 (TE)'].astype(int).mean()
        young_couples_no_children_mean = datum['Young couples without children, 2019 (TE)'].astype(int).mean()
        households_with_children_mean = datum['Households with children, 2019 (TE)'].astype(int).mean()

        one_person = result['One-person households, 2019 (TE)']
        young_single = result['Young single persons, 2019 (TE)']
        young_couples_no_children = result['Young couples without children, 2019 (TE)']
        households_with_children = result['Households with children, 2019 (TE)']

        household_structure = go.Figure()

        household_structure.add_trace(go.Indicator(
            mode="number",
            value=int(one_person),
            number={"font": {"size": 40}},
            title={"text": "One Person Households<br><span style='font-size:0.8em;color:gray'>" +
                           "All single person households</span><br>"},
            domain={'x': [0, 0.5], 'y': [0.5, 1]},
            )
        )

        household_structure.add_trace(go.Indicator(
            mode="number",
            value=int(young_single),
            number={"font": {"size": 40}},
            title={"text": "Young Single Person<br><span style='font-size:0.8em;color:gray'>" +
                           "All single person households</span><br>"},
            delta={'reference': int(young_single_mean), 'relative': True, 'position': "top"},
            domain={'x': [0.5, 1], 'y': [0.5, 1]},
            )
        )

        household_structure.add_trace(go.Indicator(
            mode="number",
            value=int(young_couples_no_children),
            number={"font": {"size": 40}},
            title={"text": "Young couples without children<br><span style='font-size:0.8em;color:gray'>" +
                           "Aged under 35 (Highest earner)</span><br>"},
            delta={'reference': int(young_couples_no_children_mean), 'relative': True, 'position': "top"},
            domain={'x': [0, 0.5], 'y': [0, 0.5]},
            )
        )

        household_structure.add_trace(go.Indicator(
            mode="number",
            value=int(households_with_children),
            number={"font": {"size": 40}},
            title={"text": "Young couples whit children<br><span style='font-size:0.8em;color:gray'>" +
                           "Aged under 35(Highest earner)</span><br>"},
            delta={'reference': int(households_with_children_mean), 'relative': True, 'position': "top"},
            domain={'x': [0.5, 1], 'y': [0, 0.5]},
            )
        )

        household_structure.update_layout(
                paper_bgcolor='#1E1E1E',
                plot_bgcolor='#1E1E1E',
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                autosize=True,
                font=dict(color="white")
            )

        text_1 = f"""
            The indicators above illustrates the structure of Household in {neighborhood} neighborhood.
            This structure is changing at a slow rate but it is not constant.
            It is affected by a multitude of social, cultural, and economic forces.
            """

        children = [
            html.H5(section_title),
            html.P("""
            Household structure refers to the generational contours and the extent of nucleation in the household.
            Nuclear arrangements(One person, young couple with children) often provide a glimpse into macro
            trends within the population.
            """),
            dcc.Graph(id='injected-indicators', figure=household_structure, config={'displayModeBar': False},),
            html.P(text_1),
        ]

        return children

    # Tab 1 Section 2 Household Income
    @dash_app.callback(
        Output('id_household_income', 'children'),
        Input('choropleth-map', 'clickData')
    )
    def display_click_data(click_data):
        """
        Generates the graphs for Household Income section.
        ---
        Args: 
            click_data (dict): dictionary returned by dcc.Graph component triggered by user-interaction.

        Returns: 
            children (list): List of html components to be displayed.
        """
        section_title = "Household Income Levels"

        # Get the postal code based on clicked area
        postal_code = get_postal_code(click_data)

        # get df row based on postal number
        result = datum.loc[postal_code]
        neighborhood = result['neighborhood']

        # Data privacy check
        if privacy_check(postal_code):
            return privacy_notice(section_title, neighborhood)

        mean_income_helsinki = datum['Average income of households, 2019 (TR)'].astype(int).mean()
        median_income_helsinki = datum['Median income of households, 2019 (TR)'].astype(int).median()

        lower_class = result['Households belonging to the lowest income category, 2019 (TR)']
        middle_class = result['Households belonging to the middle income category, 2019 (TR)']
        upper_class = result['Households belonging to the highest income category, 2019 (TR)']
        mean_income = result['Average income of households, 2019 (TR)']
        median_income = result['Median income of households, 2019 (TR)']

        # Get gender columns
        income_level_values = [lower_class, middle_class, upper_class]
        income_level_labels = ["Lower Class", "Middle Class", "Upper Class"]

        # Create pie chart figure
        income_pie_chart = go.Figure(
            data=[
                go.Pie(
                    labels=income_level_labels, 
                    values=income_level_values, 
                    hole=.7
                )
            ]
        )

        income_pie_chart.update_layout(
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-.15,
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

        income_pie_chart.update_traces(
            hoverinfo='label+percent+value',
            marker=dict(
                colors=colors,
                line=dict(
                    color='#1E1E1E',
                    width=2
                )
            )
        )

        income_indicators = go.Figure()

        income_indicators.add_trace(go.Indicator(
            mode="number",
            value=int(mean_income),
            number={'prefix': "€", "font": {"size": 40}},
            title={"text": "Avg.Household Income<br><span style='font-size:0.8em;color:gray'>" +
                           "Average Household income in postal area.</span><br>"},
            domain={'x': [0, 0.5], 'y': [.5, 1]},
            )
        )

        income_indicators.add_trace(go.Indicator(
            mode="number",
            value=int(median_income),
            number={'prefix': "€", "font": {"size": 40}},
            title={"text": "Median Household Income<br><span style='font-size:0.8em;color:gray'>" +
                           "Median Household income.</span><br>"},
            domain={'x': [0, 0.5], 'y': [0, .5]}
            )
        )

        income_indicators.add_trace(go.Indicator(
            mode="number",
            value=int(mean_income_helsinki),
            number={'prefix': "€", "font": {"size": 40}},
            title={"text": "Avg. Household Income in Helsinki<br><span style='font-size:0.8em;color:gray'>" +
                           "Average for whole Helsinki</span><br>"},
            domain={'x': [0.5, 1], 'y': [0.5, 1]}
            )
        )

        income_indicators.add_trace(go.Indicator(
            mode="number",
            value=int(median_income_helsinki),
            number={'prefix': "€", "font": {"size": 40}},
            title={"text": "Median Household Income in Helsinki<br><span style='font-size:0.8em;color:gray'>" +
                           "Median Household income in Helsinki</span><br>"},
            domain={'x': [0.5, 1], 'y': [0, .5]}
            )
        )

        income_indicators.update_layout(
                paper_bgcolor='#1E1E1E',
                plot_bgcolor='#1E1E1E',
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                autosize=True,
                font=dict(color="white")
            )

        text_1 = f"""
            The graph above illustrates the Household income levels in {neighborhood} neighborhood.
            This distribution is not constant. It is affected by a multitude of social, cultural, and economic forces.
            """
        text_2 = f"""
        The average income of an individual in {neighborhood} is {mean_income}€ per year.
        While the median income is {median_income}€ per year.
        The percentages illustrate the difference between mean and median income in Helsinki metropolitan area.
        """

        children = [
            html.H5(section_title),
            html.P("""
            Disposable household income is generally defined as the combined monetary income remaining after 
            deduction of taxes and social security charges. Income of all members of a household is taken into account.
            Note that individuals do not have to be related in any way to be considered members of the same household.
            Household income is an important risk measure used by lenders for underwriting loans and is a useful
            economic indicator of an area's standard of living.
            """),
            dcc.Graph(id='injected-indicators', figure=income_indicators, config={'displayModeBar': False},),
            html.P(text_2),
            dcc.Graph(id='injected', figure=income_pie_chart, config={'displayModeBar': False},),
            html.P(text_1),
        ]

        return children

    # Tab 1 Section 2 Household Dwellings
    @dash_app.callback(
        Output('id_household_dwellings', 'children'),
        Input('choropleth-map', 'clickData'))
    def display_click_data(click_data):
        """
        Generates the graphs for Household Dwellings section.
        ---
        Args: 
            click_data (dict): dictionary returned by dcc.Graph component triggered by user-interaction.

        Returns: 
            children (list): List of html components to be displayed.
        """
        section_title = "Household Dwellings"
        
        # Get the postal code based on clicked area
        postal_code = get_postal_code(click_data)

        # get df row based on postal number
        result = datum.loc[postal_code]
        neighborhood = result['neighborhood']

        # Data privacy check
        if privacy_check(postal_code):
            return privacy_notice(section_title, neighborhood)

        owner_occupied = result['Households living in owner-occupied dwellings, 2019 (TE)']
        rental_occupied = result['Households living in rented dwellings, 2019 (TE)']
        other_occupied = result['Households living in other dwellings, 2019 (TE)']

        values = [owner_occupied, rental_occupied, other_occupied]
        labels = ['Own House', 'Renting', 'Other']

        # Create pie chart figure
        dwellings_pie_chart = go.Figure(
            data=[
                go.Pie(
                    labels=labels, 
                    values=values, 
                    hole=.7
                )
            ]
        )
        dwellings_pie_chart.update_layout(
            showlegend=False,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=0,
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
        dwellings_pie_chart.update_traces(
            hoverinfo='label+percent+value',
            marker=dict(
                colors=colors,
                line=dict(
                    color='#1E1E1E',
                    width=2
                )
            )
        )
        text = f"""
            The graph above illustrates the ratio of rented and owned households in {neighborhood} neighborhood.  
            """

        children = [
            html.H5(section_title),
            html.P("""
            Due to a number of economic and cultural factors some households live in rental apartments 
            while other own an apartment. This section illustrates the ratio of households that own or 
            rent their primary residence.
            """),
            dcc.Graph(id='injected', figure=dwellings_pie_chart, config={'displayModeBar': False}),
            html.P(text),
        ]

        return children

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
