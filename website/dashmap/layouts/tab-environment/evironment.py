from templates.templates import init_accordion_element, assemble_accordion

def init_environment_accordion():
    """
    Initialize the accordion for environment tab.
    Args: None

    Returns: 
        census_individuals_accordion (object): dash html.Div that contains individual accordions
    """
    wind_rose = init_accordion_element(
        title="Wind Patterns", 
        id='id_windrose',
        tab_n=5, 
        group_n=1
    )

    avg_air_temp = init_accordion_element(
        title="Air Temperature",
        id='id_air_temperature',
        tab_n=5,
        group_n=2
    
    )

    air_pollution = init_accordion_element(
        title="Air Pollution",
        id='id_air_pollution',
        tab_n=5,
        group_n=3
    )

    accordions = list(
        wind_rose, 
        avg_air_temp,
        air_pollution,
    )

    return assemble_accordion(accordions)