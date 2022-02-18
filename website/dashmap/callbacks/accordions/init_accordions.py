import dash

from .census_accordion import init_census_accordions
from .real_estate_accordion import init_real_estate_accordions
from .services_accordion import init_services_accordions
from .mobility_accordion import init_mobility_accordions
from .environment_accordion import init_environment_accordions


def init_all_accordions(app: dash.Dash) -> None:
    """
    Initiates All callbacks for all tab accordions.
    ---
    Args:
        app (dash.Dash): Dash application to which the callback is registered to.

    Returns: None
    """
    init_census_accordions(app)
    init_real_estate_accordions(app)
    init_services_accordions(app)
    init_mobility_accordions(app)
    init_environment_accordions(app)
