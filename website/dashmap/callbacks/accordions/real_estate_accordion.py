
import pandas as pd
# Dash
import dash
from dash.dependencies import Input, Output, State



def init_basic_re_accordion(dash_app):
    """
    """
    # Tab Real Estate Accordion CallBacks
    @dash_app.callback(
        [Output(f"tab-2-collapse-{i}", "is_open") for i in range(2, 5)],
        [Input(f"tab-2-group-{i}-toggle", "n_clicks") for i in range(2, 5)],
        [State(f"tab-2-collapse-{i}", "is_open") for i in range(2, 5)],
    )
    def toggle_accordion(n2, n3, n4, is_open2, is_open3, is_open4):
        """
        Toggle accordion collapse & expand.
        ---
        Args: 
            n1 -> n4 (str): id of the trigger button  
            is_open1 -> is_open4 (bool): Current state of the accordion. True for Open, False otherwise.

        Returns: 
            (bool): Boolean values for each accordion tab. True for Open, False otherwise. Default value is False.
        """
        ctx = dash.callback_context

        if not ctx.triggered:
            return False, False, False
        else:
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "tab-2-group-2-toggle" and n2:
            return not is_open2, False, False
        elif button_id == "tab-2-group-3-toggle" and n3:
            return False, not is_open3, False
        elif button_id == "tab-2-group-4-toggle" and n4:
            return False, False, not is_open4

        return False, False, False


def init_real_estate_accordions(dash_app):
    """
    """
    init_basic_re_accordion(dash_app)