from ..templates.templates import init_accordion_element, assemble_accordion


def init_services_accordion():
    """
    Initialize the accordion for services tab.
    Args: None

    Returns: 
        census_individuals_accordion (object): dash html.Div that contains individual accordions
    """
    accord_industries = init_accordion_element(
        title="Industry", 
        graph_id='id_services_industries',
        tab_n=3, 
        group_n=1
    )

    accord_workplaces = init_accordion_element(
        title="Workplaces",
        graph_id='id_workplaces',
        tab_n=3,
        group_n=2
    )

    accordions = [
        accord_industries, 
        accord_workplaces,
    ]

    return assemble_accordion(accordions)
