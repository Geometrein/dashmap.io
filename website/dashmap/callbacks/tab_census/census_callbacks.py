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

def init_census_callbacks(app, datum):
    """
    """
   # Tab 1 Section 1 Age Distribution CallBack
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

        columns_list = datum.columns[index_start:index_end]
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

    # Tab 1 Section 1 Gender Distribution CallBack
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
    @app.callback(
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
    @app.callback(
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
    @app.callback(
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
    @app.callback(
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
