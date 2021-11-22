from templates.templates import init_accordion_element, assemble_accordion

def init_real_estate_accordion():
    """
    Initialize the real estate accordion for real estate tab.
    Args: None

    Returns: 
        real_estate_accordion (object): dash html.Div that contains individual accordions
    """
    accord_re_owning = init_accordion_element(
        title="Ownership", 
        id='id_re_owning', 
        tab_n=2, 
        group_n=2
    )

    accord_re_renting = init_accordion_element(
        title="Rentals", 
        id='id_re_renting', 
        tab_n=2, 
        group_n=3
    )

    accord_re_sauna = init_accordion_element(
        title="Sauna Index", 
        id='id_re_sauna', 
        tab_n=2, 
        group_n=4
    )

    accordions = list(
        accord_re_owning, 
        accord_re_renting,
        accord_re_sauna,
    )

    return assemble_accordion(accordions)