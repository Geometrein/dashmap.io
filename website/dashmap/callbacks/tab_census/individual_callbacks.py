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


def init_age_histogram(app, datum):
    """
    Tab 1 Section 1 Age Distribution CallBack
    """
    @app.callback(
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
    
        # Get df row based on postal number
        row = datum.loc[postal_code]

        # Get neighborhood name and mean age 
        neighborhood = str(row.iloc[0])
        mean_age = int(row.iloc[6])

        # Data privacy check
        if privacy_check(postal_code):
            return privacy_notice(section_title, neighborhood)

        index_start = 7      # 0-2 years
        index_end = 26 + 1  # 85 years or over

        # Neighborhood
        age_bins = row.index[index_start:index_end].tolist()
        x_age_bins = [i.split(' ')[0] for i in age_bins]
        y_neighborhood = row[index_start:index_end].astype(int).tolist()

        # Helsinki
        columns_list = datum.columns[index_start:index_end]
        y_helsinki = [datum[column].astype(float).mean() for column in columns_list]

        # Create pie chart figure object
        age_dist_hist = go.Figure(
            data=[
                go.Bar(
                    name=neighborhood,
                    x=x_age_bins, 
                    y=y_neighborhood,
                    marker=dict(
                        color='#4182C8',
                    )
                )
            ]
        )

        # Average age distribution in Helsinki
        age_dist_hist.add_trace(
            go.Bar(
                name='Helsinki Average',
                x=x_age_bins,
                y=y_helsinki,
                marker=dict(
                    color='#F3903F'
                ),
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
        
        age_dist_hist.update_traces(hoverinfo='text')
        
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


def init_gender_pie(app, datum):
    """
    Tab 1 Section 1 Gender Distribution CallBack
    """
    @app.callback(
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
        row = datum.loc[postal_code]

        # Get neighborhood name and mean age 
        neighborhood = str(row.iloc[0])

        # Data privacy check
        if privacy_check(postal_code):
            return privacy_notice(section_title, neighborhood)

        # Get number of males and females in a district
        males = int(row.iloc[4])  # Males, 20XX (HE)
        females = int(row.iloc[5])  # Females, 20XX (HE)

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


def init_education_pie(app, datum):
    """
    """
    # Tab 1 Section 1 Education Pie chart CallBack
    @app.callback(
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
        row = datum.loc[postal_code]

        # Get neighborhood name and mean age 
        neighborhood = str(row.iloc[0])

        # Data privacy check
        if privacy_check(postal_code):
            return privacy_notice(section_title, neighborhood)

        index_start = 28  # 28 Basic level studies, 20XX (KO)
        index_end = 33 + 1  # 33 Academic degree - Higher level university degree, 2020 (KO)

        education_values = row[index_start:index_end].astype(int).tolist()
        education_values.pop(1)  # remove "29 With education, total, 20XX (KO)" column

        education_labels = row.index[index_start:index_end].tolist()
        education_labels.pop(1)
        education_labels = [label.split(',')[0] for label in education_labels]

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


def init_income_indicators(app, datum):
    """
    Tab 1 Section 1 Income CallBack
    """
    @app.callback(
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

        # Get df row based on postal number
        row = datum.loc[postal_code]

        # Get neighborhood name and mean age 
        neighborhood = str(row.iloc[0])

        # Data privacy check
        if privacy_check(postal_code):
            return privacy_notice(section_title, neighborhood)
        
        mean_income_helsinki = datum.iloc[:, 35].astype(int).mean()
        median_income_helsinki = datum.iloc[:, 36].astype(int).mean()

        lower_class = row.iloc[37]  # Inhabitants belonging to the lowest income category
        middle_class = row.iloc[38]  # Inhabitants belonging to the middle income category
        upper_class = row.iloc[39]  # Inhabitants belonging to the highest income category
        mean_income = row.iloc[35]  # Average income of inhabitants
        median_income = row.iloc[35]  # Median income of inhabitants

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


def init_employment_pie(app, datum):
    """
    Tab 1 Section 1 Employment CallBack
    """
    @app.callback(
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
        row = datum.loc[postal_code]
        neighborhood = str(row.iloc[0])

        # Data privacy check
        if privacy_check(postal_code):
            return privacy_notice(section_title, neighborhood)
        
        # get relevant data
        employed = row.iloc[101]  # Employed, 20XX (PT)
        unemployed = row.iloc[102]  # Unemployed, 20XX (PT)
        # children_under_14 = row.iloc[103]  # Children aged 0 to 14, 20XX (PT)
        students = row.iloc[104]  # Students, 20XX (PT)
        pensioners = row.iloc[105]  # Pensioners, 20XX (PT)
        other = row.iloc[106]  # Others, 20XX (PT)

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
