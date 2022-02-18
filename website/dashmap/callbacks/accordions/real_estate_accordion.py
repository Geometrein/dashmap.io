from typing import Tuple

import dash
from dash.dependencies import Input, Output, State


def init_basic_re_accordion(app: dash.Dash) -> None:
    """
    Initiates TAB: Real Estate accordion callbacks.
    ---
    Args:
        app (dash.Dash): Dash application to which the callback is registered to.

    Returns: None
    """
    @app.callback(
        [Output(f"tab-2-collapse-{i}", "is_open") for i in range(1, 4)],
        [Input(f"tab-2-group-{i}-toggle", "n_clicks") for i in range(1, 4)],
        [State(f"tab-2-collapse-{i}", "is_open") for i in range(1, 4)],
    )
    def toggle_accordion(
            n1: str, n2: str, n3: str,
            is_open1: bool, is_open2: bool, is_open3: bool
    ) -> Tuple[bool, bool, bool]:
        """
        Toggle accordion collapse & expand.
        ---
        Args: 
            n1 -> n4 (str): id of the trigger button  
            is_open1 -> is_open4 (bool): Current state of the accordion. True for Open, False otherwise.

        Returns: 
            (Tuple): Tuple of Boolean values for each accordion tab.
            True for Open, False otherwise. Default value is False.
        """
        ctx = dash.callback_context

        if not ctx.triggered:
            return False, False, False
        else:
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "tab-2-group-1-toggle" and n1:
            return not is_open1, False, False
        elif button_id == "tab-2-group-2-toggle" and n2:
            return False, not is_open2, False
        elif button_id == "tab-2-group-3-toggle" and n3:
            return False, False, not is_open3

        return False, False, False


def init_real_estate_accordions(app: dash.Dash) -> None:
    """
    Initiates TAB: Real Estate Section accordion callbacks.
    ---
    Args:
        app (dash.Dash): Dash application to which the callback is registered to.

    Returns: None
    """
    init_basic_re_accordion(app)
