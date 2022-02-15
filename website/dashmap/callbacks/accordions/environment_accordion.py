import dash
from dash.dependencies import Input, Output, State



def init_basic_env_accordion(app):
    """
    """
    # Tab Environment Section Accordion CallBacks
    @app.callback(
        [Output(f"tab-5-collapse-{i}", "is_open") for i in range(1, 4)],
        [Input(f"tab-5-group-{i}-toggle", "n_clicks") for i in range(1, 4)],
        [State(f"tab-5-collapse-{i}", "is_open") for i in range(1, 4)],
    )
    def toggle_accordion(n1, n2, n3, is_open1, is_open2, is_open3):
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
            return False, False, False
        else:
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "tab-5-group-1-toggle" and n1:
            return not is_open1, False, False
        elif button_id == "tab-5-group-2-toggle" and n2:
            return False, not is_open2, False
        elif button_id == "tab-5-group-3-toggle" and n3:
            return False, False, not is_open3

        return False, False, False


def init_environment_accordions(app):
    """
    """
    init_basic_env_accordion(app)