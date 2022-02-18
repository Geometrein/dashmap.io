from typing import Tuple

import dash
from dash.dependencies import Input, Output, State


def init_individual_census_accordion(dash_app: dash.Dash) -> None:
    """
    Initiates TAB: Census Section: individuals  accordion callbacks.
    ---
    Args:
        dash_app (dash.Dash): Dash application to which the callback is registered to.

    Returns: None
    """
    @dash_app.callback(
        [Output(f"tab-1-collapse-{i}", "is_open") for i in range(1, 6)],
        [Input(f"tab-1-group-{i}-toggle", "n_clicks") for i in range(1, 6)],
        [State(f"tab-1-collapse-{i}", "is_open") for i in range(1, 6)],
    )
    def toggle_accordion(
            n1: str, n2: str, n3: str, n4: str, n5: str,
            is_open1: bool, is_open2: bool, is_open3: bool, is_open4: bool, is_open5: bool
    ) -> Tuple[bool, bool, bool, bool, bool]:
        """
        Toggle accordion collapse & expand.
        ---
        Args: 
            n1 -> n5 (str): id of the trigger button  
            is_open1 -> is_open5 (bool): Current state of the accordion. True for Open, False otherwise.

        Returns: 
            (Tuple): tuple of Boolean values for each accordion tab.
            True for Open, False otherwise. Default value is False.
        """
        ctx = dash.callback_context

        if not ctx.triggered:
            return False, False, False, False, False
        else:
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "tab-1-group-1-toggle" and n1:
            return not is_open1, False, False, False, False
        elif button_id == "tab-1-group-2-toggle" and n2:
            return False, not is_open2, False, False, False
        elif button_id == "tab-1-group-3-toggle" and n3:
            return False, False, not is_open3, False, False
        elif button_id == "tab-1-group-4-toggle" and n4:
            return False, False, False, not is_open4, False
        elif button_id == "tab-1-group-5-toggle" and n5:
            return False, False, False, False, not is_open5

        return False, False, False, False, False


def init_household_census_accordion(dash_app: dash.Dash) -> None:
    """
    Initiates TAB: Census Section: Household accordion callbacks.
    ---
    Args:
        dash_app (dash.Dash): Dash application to which the callback is registered to.

    Returns: None
    """
    @dash_app.callback(
        [Output(f"tab-1-2-collapse-{i}", "is_open") for i in range(1, 5)],
        [Input(f"tab-1-2-group-{i}-toggle", "n_clicks") for i in range(1, 5)],
        [State(f"tab-1-2-collapse-{i}", "is_open") for i in range(1, 5)],
    )
    def toggle_accordion(
            n1: str, n2: str, n3: str, n4: str,
            is_open1: bool, is_open2: bool, is_open3: bool, is_open4: bool
    ) -> Tuple[bool, bool, bool, bool]:
        """
        Toggle accordion collapse & expand.
        ---
        Args: 
            n1 -> n4 (str): id of the trigger button  
            is_open1 -> is_open4 (bool): Current state of the accordion. True for Open, False otherwise.

        Returns: 
            (bool): Boolean values for each accordion tab.
            True for Open, False otherwise. Default value is False.
        """
        ctx = dash.callback_context
        if not ctx.triggered:
            return False, False, False, False
        else:
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "tab-1-2-group-1-toggle" and n1:
            return not is_open1, False, False, False
        elif button_id == "tab-1-2-group-2-toggle" and n2:
            return False, not is_open2, False, False
        elif button_id == "tab-1-2-group-3-toggle" and n3:
            return False, False, not is_open3, False
        elif button_id == "tab-1-2-group-4-toggle" and n4:
            return False, False, False, not is_open4

        return False, False, False, False


def init_census_accordions(dash_app: dash.Dash) -> None:
    """
    Initiates TAB: Census Section: Individual & Household accordion callbacks.
    ---
    Args:
        dash_app (dash.Dash): Dash application to which the callback is registered to.

    Returns: None
    """
    init_individual_census_accordion(dash_app)
    init_household_census_accordion(dash_app)
