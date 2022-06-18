from dash import dcc, html
from pages import login


def serve_layout() -> html.Div:
    return html.Div(
        [
            dcc.Location(id="logout", refresh=True),
            html.Br(),
            html.Div(html.H2("You have been logged out - Please login")),
            html.Br(),
            html.Div([login.serve_layout()]),
            # html.Button(id="back-button", children="Go back", n_clicks=0),
        ]
    )
