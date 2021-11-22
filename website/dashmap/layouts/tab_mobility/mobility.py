from ..templates.templates import init_accordion_element, assemble_accordion

def init_mobility_accordion():
    """
    Initialize the accordion for mobility tab.
    Args: None

    Returns: 
        mobility_accordion (object): dash html.Div that contains individual accordions
    """
    accord_1 = init_accordion_element(
        title="Bus", 
        id='id_bus_accordion', 
        tab_n=4, 
        group_n=1
    )

    accord_2 = init_accordion_element(
        title="Metro", 
        id='id_metro_accordion', 
        tab_n=4, 
        group_n=2
    )

    accord_3 = init_accordion_element(
        title="Tram", 
        id='id_tram_accordion', 
        tab_n=4,
        group_n=3
    )

    accord_4 = init_accordion_element(
        title="Bikes", 
        id='id_bikes_accordion', 
        tab_n=4,
        group_n=3
    )

    mobility_accordion = [
        accord_1,
        accord_2,
        accord_3,
        accord_4
    ]

    return assemble_accordion(mobility_accordion)

