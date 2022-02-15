from dash import html
from dash.dependencies import Input, Output, State


def get_postal_code(click_data: dict) -> str:
    """
    Helper function for the callbacks
    Gets postal code from map click_data.
    ---
    Args: 
        click_data (dict): user click information

    Returns: 
        postal_code (str): Area postal code. '00180' by default.
    """

    # try to find the area by postcode
    try: 
        postal_code = str(click_data["points"][0]['location'])
    except:
        postal_code = '00180'  # Kamppi Postal code

    return postal_code


def privacy_check(postal_code: str) -> bool:
    """
    Helper function for the callbacks.
    Checks if postal code is private.
    ---
    Args: 
        postal_code (str): Area postal code.

    Returns: 
        True (bool): When postal code is in the private_list
        False (bool): When postal code is not found in the private_list
    """
    # List of private area postcodes
    private_list = ['00230', '02290', '01770']

    if postal_code in private_list:
        return True
    else:
        return False


def privacy_notice(section_title: str, neighborhood: str) -> list:
    """
    Helper function for the callbacks.
    ---
    Args: 
        section_title (str): Title of a sections
        neighborhood (str): name of the neighborhood 

    Returns: 
        children (list): List of html components to be displayed.
    """

    privacy_notice_text = f"""
            The statistical data about postal areas where less than 30 citizens live is 
            private due to possible privacy violations. Additionally the data representing 
            such a small population will not yield statistically significant insights.
            For these reason the data available for {neighborhood} neighborhood will not be displayed.
            """

    children = [
        html.H5(section_title),
        html.P(privacy_notice_text),
        html.P("Check out the other postal areas!")
    ]

    return children

def init_modal_popup(app):
    """
    """
    @app.callback(
        Output("help-modal-centered", "is_open"),
        [Input("help-open-centered", "n_clicks"), Input("help-close-centered", "n_clicks")],
        [State("help-modal-centered", "is_open")],
    )
    def toggle_modal(n1: str, n2: str, is_open: bool):
        """
        Toggle modal pop-ups.
        ---
        Args:
            n1 (str): id of the trigger button
            n2 (str): id of the trigger button
            is_open (bool): Current state of the modal. True for Open, False otherwise.

        Returns:
            is_open (bool): True for Open, False otherwise. Default value is False.
        """
        if n1 or n2:
            return not is_open
        return is_open