import dash

# Plotly Graph Objects
from .map_graphs import *

from .callbacks.util.helpers import *
from .callbacks.accordions.init_accordions import init_all_accordions

from .callbacks.tab_census.census_callbacks import init_census_callbacks
from .callbacks.tab_real_estate.real_estate_callbacks import init_re_callbacks
from .callbacks.tab_services.services_callbacks import init_services_callbacks
from .callbacks.tab_mobility.mobility_callbacks import init_mobility_callbacks
from .callbacks.tab_environment.environment_callbacks import init_env_callbacks


# Load datasets
datum, real_estate, bus_stops = load_datum()


def init_callbacks(dash_app: dash.callback_context) -> None:
    """
    Initialize Dash callbacks.
    ---
    Args: dash.callback_context

    Returns: None
    """
    # Modals & Accordions
    init_modal_popup(dash_app)
    init_all_accordions(dash_app)

    # Dashboards
    init_census_callbacks(dash_app, datum)
    init_re_callbacks(dash_app, real_estate)
    init_services_callbacks(dash_app, datum)
    init_mobility_callbacks(dash_app, datum)
    init_env_callbacks(dash_app)

 
