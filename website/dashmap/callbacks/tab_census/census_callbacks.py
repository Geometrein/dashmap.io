import dash
import geopandas as gpd
from .individual_callbacks import *
from .household_callbacks import *


def init_census_callbacks(app: dash.Dash, datum: gpd.GeoDataFrame) -> None:
    """
    Initializes Callbacks for filtering  graph objects data with the map.
    ---
    Args:
        app (dash.Dash): main dash app to which callbacks are registered.
        datum (gpd.GeoDataFrame): Geodataframe with postal area data.

    Returns: None
    """
    # Individual
    init_age_histogram(app, datum)
    init_gender_pie(app, datum)
    init_education_pie(app, datum)
    init_income_indicators(app, datum)
    init_employment_pie(app, datum)

    # Household
    init_household_size(app, datum)
    init_household_structure(app, datum)
    init_household_income(app, datum)
    init_household_dwellings(app, datum)
