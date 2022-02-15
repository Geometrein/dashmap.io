import dash
from dash.dependencies import Input, Output, State


def init_basic_services_accordion(dash_app):
    """
    """
    @dash_app.callback(
        [Output(f"tab-3-collapse-{i}", "is_open") for i in range(1, 3)],
        [Input(f"tab-3-group-{i}-toggle", "n_clicks") for i in range(1, 3)],
        [State(f"tab-3-collapse-{i}", "is_open") for i in range(1, 3)],
    )
    def toggle_accordion(n1, n2, is_open1, is_open2):
        """
        Toggle accordion collapse & expand.
        ---
        Args: 
            n1 -> n2 (str): id of the trigger button  
            is_open1 -> is_open2 (bool): Current state of the accordion. True for Open, False otherwise.

        Returns: 
            (bool): Boolean values for each accordion tab. True for Open, False otherwise. Default value is False.
        """

        ctx = dash.callback_context
        if not ctx.triggered:
            return False, False
        else:
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "tab-3-group-1-toggle" and n1:
            return not is_open1, False
        elif button_id == "tab-3-group-2-toggle" and n2:
            return False, not is_open2

        return False, False


def init_services_accordions(dash_app):
    """
    """
    init_basic_services_accordion(dash_app)
