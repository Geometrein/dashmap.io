import pandas as pd
pd.options.mode.chained_assignment = None

# Dash & Plotly
import dash
from dash import Dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State

# Plotly Graph Objects
from .map_graphs import *

# Load datasets
datum, real_estate  = load_datum()

#####################################################################################################################
#                                                      CallBacks                                                    #
#####################################################################################################################

def init_callbacks(dash_app):
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
    def toggle_modal(n1, n2, is_open):
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

    #####################################################################################################################
    #                                      Tab Census Section individuals Accordion CallBacks                           #
    #####################################################################################################################

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
            return not is_open1, False, False , False, False
        elif button_id == "tab-1-group-2-toggle" and n2:
            return False, not is_open2, False, False, False
        elif button_id == "tab-1-group-3-toggle" and n3:
            return False, False, not is_open3, False, False
        elif button_id == "tab-1-group-4-toggle" and n4:
            return False, False, False, not is_open4, False
        elif button_id == "tab-1-group-5-toggle" and n5:
            return False, False, False, False, not is_open5

        return False, False, False, False, False

    #####################################################################################################################
    #                                      Tab Census Section Households Accordion CallBacks                            #
    #####################################################################################################################

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
            return not is_open1, False, False , False
        elif button_id == "tab-1-2-group-2-toggle" and n2:
            return False, not is_open2, False, False
        elif button_id == "tab-1-2-group-3-toggle" and n3:
            return False, False, not is_open3, False
        elif button_id == "tab-1-2-group-4-toggle" and n4:
            return False, False, False, not is_open4

        return False, False, False, False

    #####################################################################################################################
    #                                      Tab Real Estate Accordion CallBacks                                          #
    #####################################################################################################################

    @dash_app.callback(
        [Output(f"tab-2-collapse-{i}", "is_open") for i in range(2, 5)],
        [Input(f"tab-2-group-{i}-toggle", "n_clicks") for i in range(2, 5)],
        [State(f"tab-2-collapse-{i}", "is_open") for i in range(2, 5)],
    )
    def toggle_accordion( n2, n3, n4, is_open2, is_open3, is_open4):
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
            return  not is_open2, False, False
        elif button_id == "tab-2-group-3-toggle" and n3:
            return  False, not is_open3, False
        elif button_id == "tab-2-group-4-toggle" and n4:
            return  False, False, not is_open4

        return  False, False, False

    #####################################################################################################################
    #                                      Tab 1 Section 1 Age Distribution CallBack                                    #
    #####################################################################################################################

    @dash_app.callback(
        Output('id_age_dist_hist', 'children'),
        Input('choropleth-map', 'clickData'))
    def display_click_data(clickData):
        """
        Generates the graphs for Age Distribution section.
        ---
        Args: 
            clickData (dict): dictionary returned by dcc.Graph component triggered by user-interaction.

        Returns: 
            children (list): List of html components to be displayed.
        """
        section_title = "Age Distribution"

        try:
            postal_code = str(clickData["points"][0]['location'])
        except TypeError:
            postal_code = '00180' # Kamppi Postal code

        # get df row based on postal number
        result = datum.loc[postal_code]
        neighborhood = result['neighborhood']

        age_bins = result.tolist()[7:27]

        # Get Helsinki Averages
        mean_age = result['Average age of inhabitants, 2019 (HE)']
        age_bins = [int(i) for i in age_bins]

        x = list(range(len(age_bins)))
        x = result.index.tolist()[7:27]
        x = [i.split(' ')[0] for i in x]

        columns_list = datum.columns[7:27]
        y2 = [datum[column].astype(float).mean() for column in columns_list]

        # Create pie chart figure object
        age_dist_hist = go.Figure(
            data=
            [
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
                name= 'Helsinki Average',
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
                x= 0.5,
            ),
            paper_bgcolor='#1E1E1E', 
            plot_bgcolor='#1E1E1E', 
            margin={"r":30,"t":30,"l":30,"b":30}, 
            autosize=True
        )
        age_dist_hist.update_traces(
            hoverinfo='text',


        )
        
        text=f"""
            Age distribution, also called Age Composition, is the proportionate numbers of persons in successive age categories in a given population.
            The graph above illustrates the age distribution in {neighborhood} neighborhood. The average age of the inhabitant in {neighborhood} area is {mean_age}.
            Age distributions differs among postal areas. Factors such as fertility, popularity of the area among certain age groups can affect the age composition of the area.
            If the right side of the histogram is bigger it means that the population is shrinking and aging. 
            """
        # list of postcodes where the data should be private
        private_list = ['00230', '02290', '01770']
        if postal_code not in private_list:
            children=[
                html.H5(section_title),
                dcc.Graph(id='injected', figure=age_dist_hist, config={'displayModeBar': False}),
                html.P(text)
            ]
        else:
            no_data_text=f"""
            The statistical data about postal areas where less than 30 citizens live is private due to possible privacy violations.
            Additionally the data representing such a small population will not yield any meaningful insights.
            For these reason the data available for {neighborhood} neighborhood will not be displayed.
            """
            children=[
                html.H5(section_title),
                html.P(no_data_text),
                html.P("Check out the other areas!")
            ]

        return children


    #####################################################################################################################
    #                                       Tab 1 Section 1 Gender Distribution CallBack                                #
    #####################################################################################################################

    @dash_app.callback(
        Output('id_gender_pie_chart', 'children'),
        Input('choropleth-map', 'clickData'))
    def display_click_data(clickData):
        """
        Generates the graphs for Gender Distribution section.
        ---
        Args: 
            clickData (dict): dictionary returned by dcc.Graph component triggered by user-interaction.

        Returns: 
            children (list): List of html components to be displayed.
        """
        try:
            postal_code = str(clickData["points"][0]['location'])
        except TypeError:
            postal_code = '00180' # Kamppi Postal code

        # get df row based on postal number
        result = datum.loc[postal_code]
        neighborhood = result['neighborhood']

        males = result['Males, 2019 (HE)']
        females = result['Females, 2019 (HE)']

        # Get gender columns
        gender_pie_chart_values = [males, females ]
        gender_pie_chart_labels = ["Males", "Females"]
        #print(gender_pie_chart_values)

        # Create pie chart figure
        gender_pie_chart = go.Figure(
            data=
            [
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
            margin={"r":30,"t":30,"l":30,"b":30}, 
            autosize=True
        )
        gender_pie_chart.update_traces(
            hoverinfo='label+percent+value',
            marker=dict(colors=['#4182C8', '#2E94B2'],#['#4fc1e9','#48cfad'],
                line=dict(
                    color='#1E1E1E',
                    width=2
                )
            )
        )
        text=f"""
            The graph above illustrates the distribution of males and females in {neighborhood} neighborhood.  
            Gender distribution has a measurable and proven impact on a wide range of societal, demographic, and the economic processes within the city.
            This distribution is not constant. It is affected by biological, social, cultural, and economic forces.
            From the graph above we can see that 
            """

        #print(gender_pie_chart_values[0],gender_pie_chart_values[1])
        if int(gender_pie_chart_values[0]) > int(gender_pie_chart_values[1]):
            text +=  f"men outnumber women in {neighborhood} neighborhood."
        elif int(gender_pie_chart_values[0]) < int(gender_pie_chart_values[1]):
            text += f"women outnumber men in {neighborhood} neighborhood."
        else:
            text += f" the distribution of men and women in the {neighborhood} neighborhood is roughly equal."

        # list of postcodes where the data should be private
        private_list = ['00230', '02290', '01770']
        if postal_code not in private_list:
            children=[
                html.H5("Gender Composition"),
                dcc.Graph(id='injected', figure=gender_pie_chart, config={'displayModeBar': False},),
                html.P(text),
            ]
        else:
            no_data_text=f"""
            The statistical data about postal areas where less than 30 citizens live is private due to possible privacy violations.
            Additionally the data representing such a small population will not yield any meaningful insights.
            For these reason the data available for {neighborhood} neighborhood will not be displayed.
            """
            children=[
                html.H5("Age Distribution"),
                html.P(no_data_text),
                html.P("Check out the other areas!")
            ]

        return children

    #####################################################################################################################
    #                                       Tab 1 Section 1 Education Pie chart CallBack                                #
    #####################################################################################################################

    @dash_app.callback(
        Output('id_education_pie_chart', 'children'),
        Input('choropleth-map', 'clickData'))
    def display_click_data(clickData):
        """
        Generates the graphs for Education section.
        ---
        Args: 
            clickData (dict): dictionary returned by dcc.Graph component triggered by user-interaction.

        Returns: 
            children (list): List of html components to be displayed.
        """
        try:
            postal_code = str(clickData["points"][0]['location'])
        except TypeError: # If postal code is not found
            postal_code = '00180' # Kamppi Postal code

        # get df row based on postal number
        result = datum.loc[postal_code]
        neighborhood = result['neighborhood']

        education_values = result.tolist()[28:34]
        education_values.pop(1) # remove "With Education" column
        education_values = [int(i) for i in education_values]

        education_labels = result.index.tolist()[28:34]
        education_labels.pop(1)
        education_labels = [i.split(',')[0] for i in education_labels]
        #print(education_labels)

        # Create pie chart figure
        education_pie_chart = go.Figure(
            data=
            [
                go.Pie(
                    labels=education_labels, 
                    values=education_values, 
                    hole=.7
                )
            ]
        )
        education_pie_chart.update_layout(
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
            margin={"r":30,"t":30,"l":30,"b":30}, 
            autosize=True
        )
        education_pie_chart.update_traces(
            hoverinfo='label+percent+value',
            marker=dict(colors=colors,
                line=dict(
                    color='#1E1E1E',
                    width=2
                )
            )
        )
        text=f"""
            The graph above illustrates the distribution of education {neighborhood} neighborhood.  

            """

        private_list = ['00230', '02290', '01770']
        if postal_code not in private_list:
            children=[
                html.H5("Education"),
                dcc.Graph(id='injected', figure=education_pie_chart, config={'displayModeBar': False},),
                html.P(text),
            ]
        else:
            no_data_text=f"""
            The statistical data about postal areas where less than 30 citizens live is private due to possible privacy violations.
            Additionally the data representing such a small population will not yield any meaningful insights.
            For these reason the data available for {neighborhood} neighborhood will not be displayed.
            """
            children=[
                html.H5("Age Distribution"),
                html.P(no_data_text),
                html.P("Check out the other areas!")
            ]

        return children

    #####################################################################################################################
    #                                           Tab 1 Section 1 Income CallBack                                         #
    #####################################################################################################################

    @dash_app.callback(
        Output('id_income_pie_chart', 'children'),
        Input('choropleth-map', 'clickData'))
    def display_click_data(clickData):
        """
        Generates the graphs for Income section.
        ---
        Args: 
            clickData (dict): dictionary returned by dcc.Graph component triggered by user-interaction.

        Returns: 
            children (list): List of html components to be displayed.
        """
        
        try:
            postal_code = str(clickData["points"][0]['location'])
        except TypeError:
            postal_code = '00180' # Kamppi Postal code

        # get df row based on postal number
        result = datum.loc[postal_code]
        neighborhood = result['neighborhood']
        mean_income_helsinki = datum['Average income of inhabitants, 2019 (HR)'].astype(int).mean()
        median_income_helsinki = datum['Average income of inhabitants, 2019 (HR)'].astype(int).median()

        lower_class = result['Inhabintants belonging to the lowest income category, 2019 (HR)'] # Name of the column contains a type Inhabintants
        middle_class = result['Inhabitants belonging to the middle income category, 2019 (HR)']
        upper_class = result['Inhabintants belonging to the highest income category, 2019 (HR)'] # Name of the column contains a typo Inhabintants
        mean_income = result['Average income of inhabitants, 2019 (HR)']
        median_income = result['Median income of inhabitants, 2019 (HR)']

        # Get gender columns
        income_level_values = [lower_class, middle_class, upper_class]
        income_level_labels = ["Lower Class", "Middle Class", "Upper Class"]
        #print(gender_pie_chart_values)

        # Create pie chart figure
        income_pie_chart = go.Figure(
            data=
            [
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
            margin={"r":30,"t":30,"l":30,"b":30}, 
            autosize=True
        )
        income_pie_chart.update_traces(
            hoverinfo='label+percent+value',
            marker=dict(colors=colors,
                line=dict(
                    color='#1E1E1E',
                    width=2
                )
            )
        )

        income_indicators = go.Figure()

        income_indicators.add_trace(go.Indicator(
            mode = "number+delta",
            value = int(mean_income),
            number = {'prefix': "€", "font":{"size":50}},
            title = {"text": "Average Income<br><span style='font-size:0.8em;color:gray'>Compared to Average income in Helsinki </span><br>"},
            domain = {'x': [0, 1], 'y': [.5, 1]},
            delta = {'reference': mean_income_helsinki, 'relative': True, 'position' : "top"}))

        income_indicators.add_trace(go.Indicator(
            mode = "number+delta",
            value = int(median_income),
            number = {'prefix': "€", "font":{"size":50}},
            title = {"text": "Median Income<br><span style='font-size:0.8em;color:gray'>Compared to Median income in Helsinki </span><br>"},
            delta = {'reference': median_income_helsinki, 'relative': True, 'position' : "top"},
            domain = {'x': [0, 1], 'y': [0, .5]}))

        income_indicators.update_layout(
                paper_bgcolor='#1E1E1E',
                plot_bgcolor='#1E1E1E',
                margin={"r":0,"t":0,"l":0,"b":0},
                autosize=True,
                font=dict(color="white")
            )

        text_1=f"""
            The graph above illustrates the class distribution of individuals in {neighborhood} neighborhood.
            This distribution is not constant. It is affected by biological, social, cultural, and economic forces.
            """
        text_2 = f"""
        The average income of an individual in {neighborhood} is {mean_income}€ per year.
        While the median income is {median_income}€ per year.
        The percentages illustrate the difference between mean and median income in Helsinki metropolitan area.
        """
        no_data_text=f"""
            The statistical data about postal areas where less than 30 citizens live is private due to possible privacy violations.
            Additionally the data representing such a small population will not yield any meaningful insights.
            For these reason the data available for {neighborhood} neighborhood will not be displayed.
            """
        # list of postcodes where the data should be private
        private_list = ['00230', '02290', '01770']
        if postal_code not in private_list:
            children=[
                html.H5("Individual Income levels"),
                dcc.Graph(id='injected-indicators', figure=income_indicators, config={'displayModeBar': False},),
                html.P(text_2),
                dcc.Graph(id='injected', figure=income_pie_chart, config={'displayModeBar': False},),
                html.P(text_1),
            ]
        else:
            children=[
                html.H5("Income Distribution"),
                html.P(no_data_text),
                html.P("Check out the other areas!")
            ]

        return children

    #####################################################################################################################
    #                                        Tab 1 Section 1 Employment CallBack                                        #
    #####################################################################################################################

    @dash_app.callback(
        Output('id_employment_pie_chart', 'children'),
        Input('choropleth-map', 'clickData'))
    def display_click_data(clickData):
        """
        Generates the graphs for Employment section.
        ---
        Args: 
            clickData (dict): dictionary returned by dcc.Graph component triggered by user-interaction.

        Returns: 
            children (list): List of html components to be displayed.
        """
        try:
            postal_code = str(clickData["points"][0]['location'])
        except TypeError:
            postal_code = '00180' # Kamppi Postal code

        # get df row based on postal number
        result = datum.loc[postal_code]
        neighborhood = result['neighborhood']

        employed = result['Employed, 2018 (PT)']
        unemployed = result['Unemployed, 2018 (PT)']
        students = result['Students, 2018 (PT)']
        pensioners = result['Pensioners, 2018 (PT)']
        other = result['Others, 2018 (PT)']
        children_under_14 = ['Children aged 0 to 14, 2018 (PT)']


        # Get gender columns
        emploment_level_values = [employed,unemployed, pensioners, students, other]
        emploment_level_labels = ["Employed", "Unemployed", "Pensioners", "Students", "Other"]
        #print(gender_pie_chart_values)

        # Create pie chart figure
        income_pie_chart = go.Figure(
            data=
            [
                go.Pie(
                    labels=emploment_level_labels, 
                    values=emploment_level_values, 
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
            margin={"r":30,"t":30,"l":30,"b":30}, 
            autosize=True
        )
        income_pie_chart.update_traces(
            hoverinfo='label+percent+value',
            marker=dict(colors=colors,
                line=dict(
                    color='#1E1E1E',
                    width=2
                )
            )
        )

        text_1=f"""
            The graph above illustrates the class employment status of individuals in {neighborhood} neighborhood.
            This distribution is not constant. It is affected by biological, social, cultural, and economic forces.
            """
        no_data_text=f"""
            The statistical data about postal areas where less than 30 citizens live is private due to possible privacy violations.
            Additionally the data representing such a small population will not yield any meaningful insights.
            For these reason the data available for {neighborhood} neighborhood will not be displayed.
            """
        # list of postcodes where the data should be private
        private_list = ['00230', '02290', '01770']
        if postal_code not in private_list:
            children=[
                html.H5("Employment Status"),
                dcc.Graph(id='injected', figure=income_pie_chart, config={'displayModeBar': False},),
                html.P(text_1),
            ]
        else:
            children=[
                html.H5("Income Distribution"),
                html.P(no_data_text),
                html.P("Check out the other areas!")
            ]

        return children

    #####################################################################################################################
    #                                          Tab 1 Section 2 Household Size                                      #
    #####################################################################################################################
    @dash_app.callback(
        Output('id_household_size', 'children'),
        Input('choropleth-map', 'clickData'))
    def display_click_data(clickData):
        """
        Generates the graphs for Household Size section.
        ---
        Args: 
            clickData (dict): dictionary returned by dcc.Graph component triggered by user-interaction.

        Returns: 
            children (list): List of html components to be displayed.
        """
        section_title = "Household Size"


        try:
            postal_code = str(clickData["points"][0]['location'])
        except TypeError:
            postal_code = '00180' # Kamppi Postal code

        # get df row based on postal number
        result = datum.loc[postal_code]
        neighborhood = result['neighborhood']
        helsinki_mean_household_size = datum['Average size of households, 2019 (TE)'].astype(float).mean()
        helsinki_mean_occupancy_rate = datum['Occupancy rate, 2019 (TE)'].astype(float).mean()

        households_total = result['Households, total, 2019 (TE)']
        mean_household_size = result['Average size of households, 2019 (TE)']
        occupancy_rate = result['Occupancy rate, 2019 (TE)']
        


        household_basic_indicators = go.Figure()

        household_basic_indicators.add_trace(go.Indicator(
            mode = "number+delta",
            value = int(households_total),
            number = {"font":{"size":50}},
            title = {"text": "Total Households<br><span style='font-size:0.8em;color:gray'>In Helsinki metropolitan area</span><br>"},
            domain = {'x': [0, 1], 'y': [.5, 1]},
            )
        )

        household_basic_indicators.add_trace(go.Indicator(
            mode = "number+delta",
            value = float(mean_household_size),
            number = {"font":{"size":50}},
            title = {"text": "Average Household Size<br><span style='font-size:0.8em;color:gray'>Average number of people in a single household</span><br>"},
            domain = {'x': [0, .5], 'y': [0, .5]},
            delta = {'reference': helsinki_mean_household_size, 'relative': True, 'position' : "top"}
            )
        )

        household_basic_indicators.add_trace(go.Indicator(
            mode = "number+delta",
            value = float(occupancy_rate),
            number = {'suffix': ' m²',"font":{"size":50}},
            title = {"text": "Occupancy Rate<br><span style='font-size:0.8em;color:gray'>Total floor area / number of inhabitants.</span><br>"},
            domain = {'x': [.5, 1], 'y': [0, .5]},
            delta = {'reference': helsinki_mean_occupancy_rate, 'relative': True, 'position' : "top"}
            )
        )

        household_basic_indicators.update_layout(
                paper_bgcolor='#1E1E1E',
                plot_bgcolor='#1E1E1E',
                margin={"r":0,"t":0,"l":0,"b":0},
                autosize=True,
                font=dict(color="white")
            )

        text_1=f"""
            The indicators above illustrates the class distribution of individuals in {neighborhood} neighborhood.
            This distribution is not constant. It is affected by biological, social, cultural, and economic forces.
            """
        no_data_text=f"""
            The statistical data about postal areas where less than 30 citizens live is private due to possible privacy violations.
            Additionally the data representing such a small population will not yield any meaningful insights.
            For these reason the data available for {neighborhood} neighborhood will not be displayed.
            """
        # list of postcodes where the data should be private
        private_list = ['00230', '02290', '01770']
        if postal_code not in private_list:
            children=[
                html.H5("Household Size"),
                dcc.Graph(id='injected-indicators', figure=household_basic_indicators, config={'displayModeBar': False},),
                html.P(text_1),
            ]
        else:
            children=[
                html.H5("Income Distribution"),
                html.P(no_data_text),
                html.P("Check out the other areas!")
            ]

        return children

    #####################################################################################################################
    #                                          Tab 1 Section 2 Household Structure                                      #
    #####################################################################################################################

    @dash_app.callback(
        Output('id_household_structure', 'children'),
        Input('choropleth-map', 'clickData'))
    def display_click_data(clickData):
        """
        Generates the graphs for Household Structure section.
        ---
        Args: 
            clickData (dict): dictionary returned by dcc.Graph component triggered by user-interaction.

        Returns: 
            children (list): List of html components to be displayed.
        """
        section_title = "Household Structure"
        
        try:
            postal_code = str(clickData["points"][0]['location'])
        except TypeError:
            postal_code = '00180' # Kamppi Postal code

        # get df row based on postal number
        result = datum.loc[postal_code]
        neighborhood = result['neighborhood']

        # mean values
        one_person_mean = datum['One-person households, 2019 (TE)'].astype(int).mean()
        young_single_mean = datum['Young single persons, 2019 (TE)'].astype(int).mean()
        young_couples_no_children_mean = datum['Young couples without children, 2019 (TE)'].astype(int).mean()
        households_with_children_mean = datum['Households with children, 2019 (TE)'].astype(int).mean()

        one_person = result['One-person households, 2019 (TE)']
        young_single = result['Young single persons, 2019 (TE)']
        young_couples_no_children = result['Young couples without children, 2019 (TE)']
        households_with_children = result['Households with children, 2019 (TE)']

        household_structure = go.Figure()

        household_structure.add_trace(go.Indicator(
            mode = "number+delta",
            value = int(one_person),
            number = {"font":{"size":40}},
            title = {"text": "One Person Households<br><span style='font-size:0.8em;color:gray'>All single person households</span><br>"},
            delta = {'reference': int(one_person_mean), 'relative': True, 'position' : "top"},
            domain = {'x': [0, 0.5], 'y': [0.5, 1]},
            )
        )
        household_structure.add_trace(go.Indicator(
            mode = "number+delta",
            value = int(young_single),
            number = {"font":{"size":40}},
            title = {"text": "Young Single Person<br><span style='font-size:0.8em;color:gray'>All single person households</span><br>"},
            delta = {'reference': int(young_single_mean), 'relative': True, 'position' : "top"},
            domain = {'x': [0.5, 1], 'y': [0.5, 1]},
            )
        )
        household_structure.add_trace(go.Indicator(
            mode = "number+delta",
            value = int(young_couples_no_children),
            number = {"font":{"size":40}},
            title = {"text": "Young couples whitout children<br><span style='font-size:0.8em;color:gray'>Aged under 35 (Highest earner)</span><br>"},
            delta = {'reference': int(young_couples_no_children_mean), 'relative': True, 'position' : "top"},
            domain = {'x': [0, 0.5], 'y': [0, 0.5]},
            )
        )
        household_structure.add_trace(go.Indicator(
            mode = "number+delta",
            value = int(households_with_children),
            number = {"font":{"size":40}},
            title = {"text": "Young couples whit children<br><span style='font-size:0.8em;color:gray'>Aged under 35(Highest earner)</span><br>"},
            delta = {'reference': int(households_with_children_mean), 'relative': True, 'position' : "top"},
            domain = {'x': [0.5, 1], 'y': [0, 0.5]},
            )
        )

        household_structure.update_layout(
                paper_bgcolor='#1E1E1E',
                plot_bgcolor='#1E1E1E',
                margin={"r":0,"t":0,"l":0,"b":0},
                autosize=True,
                font=dict(color="white")
            )

        text_1=f"""
            The indicators above illustrates the structure of Househods in {neighborhood} neighborhood.
            This distribution is not constant. It is affected by biological, social, cultural, and economic forces.
            """
        no_data_text=f"""
            The statistical data about postal areas where less than 30 citizens live is private due to possible privacy violations.
            Additionally the data representing such a small population will not yield any meaningful insights.
            For these reason the data available for {neighborhood} neighborhood will not be displayed.
            """
        # list of postcodes where the data should be private
        private_list = ['00230', '02290', '01770']
        if postal_code not in private_list:
            children=[
                html.H5("Household Structure"),
                dcc.Graph(id='injected-indicators', figure=household_structure, config={'displayModeBar': False},),
                html.P(text_1),
            ]
        else:
            children=[
                html.H5("Income Distribution"),
                html.P(no_data_text),
                html.P("Check out the other areas!")
            ]

        return children

    #####################################################################################################################
    #                                          Tab 1 Section 2 Household Income                                         #
    #####################################################################################################################
    @dash_app.callback(
        Output('id_household_income', 'children'),
        Input('choropleth-map', 'clickData'))
    def display_click_data(clickData):
        """
        Generates the graphs for Household Income section.
        ---
        Args: 
            clickData (dict): dictionary returned by dcc.Graph component triggered by user-interaction.

        Returns: 
            children (list): List of html components to be displayed.
        """

        try:
            postal_code = str(clickData["points"][0]['location'])
        except TypeError:
            postal_code = '00180' # Kamppi Postal code

        # get df row based on postal number
        result = datum.loc[postal_code]
        neighborhood = result['neighborhood']
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
        #print(gender_pie_chart_values)

        # Create pie chart figure
        income_pie_chart = go.Figure(
            data=
            [
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
            margin={"r":30,"t":30,"l":30,"b":30}, 
            autosize=True
        )
        income_pie_chart.update_traces(
            hoverinfo='label+percent+value',
            marker=dict(colors=colors,
                line=dict(
                    color='#1E1E1E',
                    width=2
                )
            )
        )

        income_indicators = go.Figure()

        income_indicators.add_trace(go.Indicator(
            mode = "number+delta",
            value = int(mean_income),
            number = {'prefix': "€", "font":{"size":50}},
            title = {"text": "Average Household Income<br><span style='font-size:0.8em;color:gray'>Compared to Average income in Helsinki </span><br>"},
            domain = {'x': [0, 1], 'y': [.5, 1]},
            delta = {'reference': mean_income_helsinki, 'relative': True, 'position' : "top"}
            )
        )

        income_indicators.add_trace(go.Indicator(
            mode = "number+delta",
            value = int(median_income),
            number = {'prefix': "€", "font":{"size":50}},
            title = {"text": "Median Household Income<br><span style='font-size:0.8em;color:gray'>Compared to Median income in Helsinki </span><br>"},
            delta = {'reference': median_income_helsinki, 'relative': True, 'position' : "top"},
            domain = {'x': [0, 1], 'y': [0, .5]}
            )
        )

        income_indicators.update_layout(
                paper_bgcolor='#1E1E1E',
                plot_bgcolor='#1E1E1E',
                margin={"r":0,"t":0,"l":0,"b":0},
                autosize=True,
                font=dict(color="white")
            )

        text_1=f"""
            The graph above illustrates the class distribution of individuals in {neighborhood} neighborhood.
            This distribution is not constant. It is affected by biological, social, cultural, and economic forces.
            """
        text_2 = f"""
        The average income of an individual in {neighborhood} is {mean_income}€ per year.
        While the median income is {median_income}€ per year.
        The percentages illustrate the difference between mean and median income in Helsinki metropolitan area.
        """
        no_data_text=f"""
            The statistical data about postal areas where less than 30 citizens live is private due to possible privacy violations.
            Additionally the data representing such a small population will not yield any meaningful insights.
            For these reason the data available for {neighborhood} neighborhood will not be displayed.
            """
        # list of postcodes where the data should be private
        private_list = ['00230', '02290', '01770']
        if postal_code not in private_list:
            children=[
                html.H5("Household Income Levels"),
                dcc.Graph(id='injected-indicators', figure=income_indicators, config={'displayModeBar': False},),
                html.P(text_2),
                dcc.Graph(id='injected', figure=income_pie_chart, config={'displayModeBar': False},),
                html.P(text_1),
            ]
        else:
            children=[
                html.H5("Income Distribution"),
                html.P(no_data_text),
                html.P("Check out the other areas!")
            ]


        return children

    #####################################################################################################################
    #                                          Tab 1 Section 2 Household Dwellings                                      #
    #####################################################################################################################
    @dash_app.callback(
        Output('id_household_dwellings', 'children'),
        Input('choropleth-map', 'clickData'))
    def display_click_data(clickData):
        """
        Generates the graphs for Household Dwellings section.
        ---
        Args: 
            clickData (dict): dictionary returned by dcc.Graph component triggered by user-interaction.

        Returns: 
            children (list): List of html components to be displayed.
        """
        section_title = "Household Dwellings"
        
        try:
            postal_code = str(clickData["points"][0]['location'])
        except TypeError:
            postal_code = '00180' # Kamppi Postal code

        # get df row based on postal number
        result = datum.loc[postal_code]
        neighborhood = result['neighborhood']

        owner_occupied = result['Households living in owner-occupied dwellings, 2019 (TE)']
        rental_occupied = result['Households living in rented dwellings, 2019 (TE)']
        other_occupied = result['Households living in other dwellings, 2019 (TE)']

        values = [owner_occupied, rental_occupied, other_occupied]
        labels = ['Own House', 'Renting', 'Other']

        # Create pie chart figure
        education_pie_chart = go.Figure(
            data=
            [
                go.Pie(
                    labels=labels, 
                    values=values, 
                    hole=.7
                )
            ]
        )
        education_pie_chart.update_layout(
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
            margin={"r":30,"t":30,"l":30,"b":30}, 
            autosize=True
        )
        education_pie_chart.update_traces(
            hoverinfo='label+percent+value',
            marker=dict(colors=colors,
                line=dict(
                    color='#1E1E1E',
                    width=2
                )
            )
        )
        text=f"""
            The graph above illustrates the distribution of education {neighborhood} neighborhood.  
            """
        private_list = ['00230', '02290', '01770']
        if postal_code not in private_list:
            children=[
                html.H5("Households by dwellings"),
                dcc.Graph(id='injected', figure=education_pie_chart, config={'displayModeBar': False},),
                html.P(text),
            ]
        else:
            no_data_text=f"""
            The statistical data about postal areas where less than 30 citizens live is private due to possible privacy violations.
            Additionally the data representing such a small population will not yield any meaningful insights.
            For these reason the data available for {neighborhood} neighborhood will not be displayed.
            """
            children=[
                html.H5("Households by dwellings"),
                html.P(no_data_text),
                html.P("Check out the other areas!")
            ]

        return children

    #####################################################################################################################
    #                                           Tab 2 Section 1 Rental Dwellings                                        #
    #####################################################################################################################
    
    @dash_app.callback(
        Output('id_re_renting', 'children'),
        Input('choropleth-map', 'clickData'))
    def display_click_data(clickData):
        """
        #TODO if there are no enough records don't show anything
        """
        try:
            postal_code = str(clickData["points"][0]['location'])
        except TypeError:
            postal_code = '00180' # Kamppi Postal code

        rentals = real_estate[real_estate['deal_type']=='rent']

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
            mode = "number",
            value = price_per_square,
            number = {'prefix': "€", "font":{"size":50}},
            title = {"text": f"Rent per m² in {neighborhood}<br><span style='font-size:0.8em;color:gray'>Average monthly rent by square meter</span><br>"},
            domain = {'x': [0, 0.5], 'y': [0.5, 1]}
            )
        )

        rent_indicators.add_trace(go.Indicator(
            mode = "number",
            value = hels_avg_price_per_square,
            number = {'prefix': "€", "font":{"size":50}},
            title = {"text": "Average Rent in Helsinki<br><span style='font-size:0.8em;color:gray'>Average monthly rent by square meter for Helsinki </span><br>"},
            domain = {'x': [0.5, 1], 'y': [0.5, 1]},
            )
        )

        rent_indicators.add_trace(go.Indicator(
            mode = "number",
            value = hels_avg_re_area,
            number = {'suffix': " m²", "font":{"size":50}},
            title = {"text": "Average Area in Helsinki<br><span style='font-size:0.8em;color:gray'>Compared to Median income in Helsinki </span><br>"},
            domain = {'x': [0.5, 1], 'y': [0, .5]},
            )
        )
        rent_indicators.add_trace(go.Indicator(
            mode = "number",
            value = average_area,
            number = {'suffix': " m²", "font":{"size":50}},
            title = {"text": f"Average area in {neighborhood}<br><span style='font-size:0.8em;color:gray'>Compared to Median income in Helsinki </span><br>"},
            domain = {'x': [0, 0.5], 'y': [0, 0.5]},
            )
        )

        rent_indicators.update_layout(
                paper_bgcolor='#1E1E1E',
                plot_bgcolor='#1E1E1E',
                margin={"r":0,"t":0,"l":0,"b":0},
                autosize=True,
                font=dict(color="white")
            )

        children=[
            html.H5("Rental Apartments"),
            html.P(
                """
                Residential rental property refers to homes that are purchased by an 
                investor and inhabited by tenants on a lease or other type of rental agreement. 
                Residential property is property zoned specifically for living or dwelling for 
                individuals or households; it may include standalone single-family dwellings to large, 
                multi-unit apartment buildings.
                """
            ),
            dcc.Graph(id='injected', figure=rent_indicators, config={'displayModeBar': False}),
            html.P(
                """
                Above you can see the comparison of rental prices 
                """
            ),
        ]

        return children

    #####################################################################################################################
    #                                           Tab 2 Section 1 Owned Dwellings                                         #
    #####################################################################################################################
    
    @dash_app.callback(
        Output('id_re_owning', 'children'),
        Input('choropleth-map', 'clickData'))
    def display_click_data(clickData):
        """
        #TODO if there are no enough records don't show anything
        """
        try:
            postal_code = str(clickData["points"][0]['location'])
        except TypeError:
            postal_code = '00180' # Kamppi Postal code

        selling = real_estate[real_estate['deal_type']=='sell']
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
        hels_med_price_per_square = selling['price_per_square'].median()

        hels_avg_re_area = selling['area'].mean()

        sell_indicators = go.Figure()

        sell_indicators.add_trace(go.Indicator(
            mode = "number",
            value = price_per_square,
            number = {'prefix': "€", "font":{"size":40}},
            title = {"text": f"Rent per m² in {neighborhood}<br><span style='font-size:0.8em;color:gray'>Average monthly rent by square meter</span><br>"},
            domain = {'x': [0, 0.5], 'y': [0.5, 1]}
            )
        )
        sell_indicators.add_trace(go.Indicator(
            mode = "number",
            value = hels_avg_price_per_square,
            number = {'prefix': "€", "font":{"size":40}},
            title = {"text": "Average Rent in Helsinki<br><span style='font-size:0.8em;color:gray'>Average monthly rent by square meter for Helsinki </span><br>"},
            domain = {'x': [0.5, 1], 'y': [0.5, 1]},
            )
        )
        sell_indicators.add_trace(go.Indicator(
            mode = "number",
            value = hels_avg_re_area,
            number = {'suffix': " m²", "font":{"size":40}},
            title = {"text": "Average Area in Helsinki<br><span style='font-size:0.8em;color:gray'>Compared to Median income in Helsinki </span><br>"},
            domain = {'x': [0.5, 1], 'y': [0, .5]},
            )
        )
        sell_indicators.add_trace(go.Indicator(
            mode = "number",
            value = average_area,
            number = {'suffix': " m²", "font":{"size":40}},
            title = {"text": f"Average area in {neighborhood}<br><span style='font-size:0.8em;color:gray'>Compared to Median income in Helsinki </span><br>"},
            domain = {'x': [0, 0.5], 'y': [0, 0.5]},
            )
        )
        sell_indicators.update_layout(
            paper_bgcolor='#1E1E1E',
            plot_bgcolor='#1E1E1E',
            margin={"r":0,"t":0,"l":0,"b":0},
            autosize=True,
            font=dict(color="white")
            )
        
        children=[
            html.H5("Rental Apartments"),
            html.P(
                """
                Residential rental property refers to homes that are purchased by an 
                investor and inhabited by tenants on a lease or other type of rental agreement. 
                Residential property is property zoned specifically for living or dwelling for 
                individuals or households; it may include standalone single-family dwellings to large, 
                multi-unit apartment buildings.
                """
            ),
            dcc.Graph(id='injected',
                figure=sell_indicators,
                config={'displayModeBar': False}
            ),
            html.P(
                """
                Above you can see the comparison of rental prices 
                """
            ),
        ]

        return children

    #####################################################################################################################
    #                                            Tab 2 Section 1 Sauna Index                                            #
    #####################################################################################################################
    
    @dash_app.callback(
        Output('id_re_sauna', 'children'),
        Input('choropleth-map', 'clickData'))
    def display_click_data(clickData):
        """
        #TODO if there are no enough records don't show anything
        """
        try:
            postal_code = str(clickData["points"][0]['location'])
        except TypeError:
            postal_code = '00180' # Kamppi Postal code


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

        number_of_saunas = len(df[df['sauna']==True])
        sauna = go.Figure()

        sauna.add_trace(go.Indicator(
            mode = "number",
            value = number_of_saunas,
            number = {'prefix': "#",},
            title = {"text": f"Sauna index{neighborhood}<br><span style='font-size:0.8em;color:gray'>Number of known saunas in the area</span><br>"},
            )
        )
        sauna.update_layout(
            paper_bgcolor='#1E1E1E',
            plot_bgcolor='#1E1E1E',
            margin={"r":0,"t":0,"l":0,"b":0},
            autosize=True,
            font=dict(color="white")
            )

        private_list = ['00230', '02290', '01770']
        if postal_code not in private_list:
            children=[
                html.H5("Dashmap Sauna Index"),
                html.P(
                    """
                    Dashmap Sauna index is a cutting edge urban metrics that highlights the number of available saunas in the postal code area.
                    If leveraged properly this revolutionary metrics can boost your productivity.
                    """
                ),
                dcc.Graph(id='injected', figure=sauna, config={'displayModeBar': False},),

            ]
        else:
            no_data_text=f"""
            The statistical data about postal areas where less than 30 citizens live is private due to possible privacy violations.
            Additionally the data representing such a small population will not yield any meaningful insights.
            For these reason the data available for {neighborhood} neighborhood will not be displayed.
            """
            children=[
                html.H5("Age Distribution"),
                html.P(no_data_text),
                html.P("Check out the other areas!")
            ]

        return children