from ..templates.templates import init_accordion_element, assemble_accordion


def init_census_household_accordion() -> object:
    """
    Initialize the accordion for census tab.
    Args: None

    Returns: 
        (object): dash html.Div that contains individual accordions
    """
    accord_household_size = init_accordion_element(
        title="Household Size", 
        graph_id='id_household_size',
        tab_n='1-2', 
        group_n=1
    )

    accord_household_structure = init_accordion_element(
        title="Household Structure",
        graph_id='id_household_structure',
        tab_n='1-2',
        group_n=2
    )
    
    accord_household_income = init_accordion_element(
        title="Household Income",
        graph_id='id_household_income',
        tab_n='1-2',
        group_n=3
    )

    accord_household_dwell = init_accordion_element(
        title="Household Dwelling Type",
        graph_id='id_household_dwellings',
        tab_n='1-2',
        group_n=4
    )

    accordions = [
        accord_household_size, 
        accord_household_structure,
        accord_household_income,
        accord_household_dwell,
    ]

    return assemble_accordion(accordions)
