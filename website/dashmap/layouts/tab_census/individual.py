from ..templates.templates import init_accordion_element, assemble_accordion

def init_census_individual_accordion() -> object:
    """
    Initialize the accordion for census tab.
    Args: None

    Returns: 
        (object): dash html.Div that contains individual accordions
    """
    accordion_age = init_accordion_element(
        title="Age", 
        id='id_age_dist_hist', 
        tab_n=1, 
        group_n=1
    )

    accordion_gender = init_accordion_element(
        title="Gender",
        id='id_gender_pie_chart',
        tab_n=1,
        group_n=2
    )
    
    accordion_education = init_accordion_element(
        title="Education",
        id='id_education_pie_chart',
        tab_n=1,
        group_n=3
    )

    accordion_income = init_accordion_element(
        title="Income",
        id='id_income_pie_chart',
        tab_n=1,
        group_n=4
    )

    accordion_employment = init_accordion_element(
        title="Employment",
        id='id_employment_pie_chart',
        tab_n=1,
        group_n=5
    )

    accordions = [
        accordion_age, 
        accordion_gender,
        accordion_education,
        accordion_income,
        accordion_employment,
    ]

    return assemble_accordion(accordions)