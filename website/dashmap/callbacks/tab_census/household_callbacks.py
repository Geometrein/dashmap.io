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


def init_household_size(app, datum):
    """
    Tab 1 Section 2 Household Size
    """

    @app.callback(
        Output('id_household_size', 'children'),
        Input('choropleth-map', 'clickData')
    )
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

        # Get df row based on postal number
        row = datum.loc[postal_code]

        # Get neighborhood name and mean age 
        neighborhood = str(row.iloc[0])

        # Data privacy check
        if privacy_check(postal_code):
            return privacy_notice(section_title, neighborhood)
        
        helsinki_mean_household_size = datum.iloc[:, 42].astype(float).mean()  # Average size of households, 20XX (TE)
        helsinki_mean_occupancy_rate = datum.iloc[:, 43].astype(float).mean()  # Occupancy rate, 20XX (TE)

        households_total = int(row.iloc[41])  # Households, total, 20XX (TE)
        mean_household_size = float(row.iloc[42])  # Average size of households, 20XX (TE)
        occupancy_rate = float(row.iloc[43])  # Occupancy rate, 20XX (TE)
        
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


def init_household_structure(app, datum):
    """
    Tab 1 Section 2 Household Structure
    """
    @app.callback(
        Output('id_household_structure', 'children'),
        Input('choropleth-map', 'clickData')
    )
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

        # Get df row based on postal number
        row = datum.loc[postal_code]

        # Get neighborhood name and mean age 
        neighborhood = str(row.iloc[0])

        # Data privacy check
        if privacy_check(postal_code):
            return privacy_notice(section_title, neighborhood)

        # mean values
        young_single_mean = datum.iloc[:, 45].astype(int).mean()  # Young single persons
        young_couples_no_children_mean = datum.iloc[:, 46].astype(int).mean()  # Young couples without children
        households_with_children_mean = datum.iloc[:, 47].astype(int).mean()  # Households with children

        one_person = int(row.iloc[44])  # One-person households, 20XX (TE)
        young_single = int(row.iloc[45])  # Young single persons, 20XX (TE)
        young_couples_no_children = int(row.iloc[46])  # Young couples without children, 20XX (TE)
        households_with_children = int(row.iloc[47])  # Households with children, 20XX (TE)

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


def init_household_income(app, datum):
    """
    """
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

        # Get df row based on postal number
        row = datum.loc[postal_code]

        # Get neighborhood name and mean age 
        neighborhood = str(row.iloc[0])

        # Data privacy check
        if privacy_check(postal_code):
            return privacy_notice(section_title, neighborhood)

        mean_income_helsinki = datum.iloc[:, 59].astype(int).mean()  # Average income of households, 20XX (TR)
        median_income_helsinki = datum.iloc[:, 60].astype(int).mean()  # Median income of households, 20XX (TR)

        lower_class = int(row.iloc[61])  # Households belonging to the lowest income category, 20XX (TR)
        middle_class = int(row.iloc[62])  # Households belonging to the middle income category, 20XX (TR)
        upper_class = int(row.iloc[63])  # Households belonging to the highest income category, 20XX (TR)
        mean_income = int(row.iloc[59])  # Average income of households, 20XX (TR)
        median_income = int(row.iloc[60])  # Median income of households, 20XX (TR)

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


def init_household_dwellings(app, datum):
    """
    Tab 1 Section 2 Household Dwellings
    """
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

        # Get df row based on postal number
        row = datum.loc[postal_code]

        # Get neighborhood name and mean age 
        neighborhood = str(row.iloc[0])

        # Data privacy check
        if privacy_check(postal_code):
            return privacy_notice(section_title, neighborhood)

        owner_occupied = int(row.iloc[55])  # Households living in owner-occupied dwellings, 20XX (TE)
        rental_occupied = int(row.iloc[56])  # Households living in rented dwellings, 20XX (TE)
        other_occupied = int(row.iloc[57])  # Households living in other dwellings, 20XX (TE)

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
