from dash import html
import dash_bootstrap_components as dbc

def init_navbar():
    """
    Initialize the navbar inside te dash app.
    Args: None

    Returns: 
        navbar (object): dash bootstrap component NavbarSimple()
    """
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/", external_link=True)),
            dbc.NavItem(dbc.NavLink("Support", href="/support", external_link=True)),
            
            dbc.Button(
                "Help", 
                id="help-open-centered",
                color="link",
                size="sm",
                className="mr-1",
                outline=True,
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader("🎊 Welcome to Dashmap! 🎊 "),
                    dbc.ModalBody(
                        children=[
                            html.Img(
                                src='assets/help.gif', 
                                style = {
                                    'display': 'block',
                                    'margin-left': 'auto',
                                    'margin-right': 'auto',
                                    'width': '100%'
                                }
                            ),
                            html.P(
                                """
                                Use the map to filter the data by postal area.
                                You can select a postal area by clicking on it on the map. Double click will select all postal areas.
                                The data displayed on the map can be filtered too. Click on the legend of the map to show/Hide different layers.
                                """
                            )
                        ]
                    ),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Got it!",
                            id="help-close-centered",
                            className="ml-auto",
                            n_clicks=0,
                        )
                    ),
                ],
                id="help-modal-centered",
                size="lg",
                centered=True,
                is_open=False,
            ), 
        ],
        brand="Dashmap",
        brand_href="/",
        color="#1a1c22",
        dark=True,
        fluid =True
    )

    return navbar