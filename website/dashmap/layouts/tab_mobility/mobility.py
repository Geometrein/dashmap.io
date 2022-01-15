from ..templates.templates import init_accordion_element, assemble_accordion


def init_mobility_accordion():
    """
    Initialize the accordion for mobility tab.
    Args: None

    Returns: 
        mobility_accordion (object): dash html.Div that contains individual accordions
    """
    accord_1 = init_accordion_element(
        title="Mobility Index", 
        graph_id='id_mobility_index',
        tab_n=4,
        group_n=1
    )

    accord_2 = init_accordion_element(
        title="Coming Soon!",
        graph_id='id_metro_accordion',
        tab_n=4, 
        group_n=2
    )

    mobility_accordion = [
        accord_1,
        accord_2,

    ]

    return assemble_accordion(mobility_accordion)
