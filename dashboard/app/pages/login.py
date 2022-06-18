from dash import dcc, html
from dash.dependencies import Input, Output, State
from models_items.models import RegisteredUser
from flask_login import login_user
from werkzeug.security import check_password_hash
from app import RegisteredUser
from app import session, app


def serve_layout() -> html.Div:
    return html.Div(
        [
            dcc.Location(id="url_login", refresh=True),
            html.H2("""Please log in to continue:""", id="h1"),
            dcc.Input(placeholder="Enter your username", type="text", id="uname-box"),
            dcc.Input(placeholder="Enter your password", type="password", id="pwd-box"),
            html.Button(children="Login", n_clicks=0, type="submit", id="login-button"),
            html.Div(children="", id="output-state"),
        ],
        style={"display": "flex", "justifyContent": "center"},
    )


@app.callback(
    Output("url_login", "pathname"),
    [Input("login-button", "n_clicks")],
    [State("uname-box", "value"), State("pwd-box", "value")],
)
def successful(n_clicks, username_input, password_input):
    user = session.query(RegisteredUser).filter_by(username=username_input).first()
    if user:
        if check_password_hash(user.password, password_input):
            login_user(user)
            return "/home"
        else:
            pass
    else:
        pass


@app.callback(
    Output("output-state", "children"),
    [Input("login-button", "n_clicks")],
    [State("uname-box", "value"), State("pwd-box", "value")],
)
def update_output(n_clicks, username_input, password_input):
    if n_clicks > 0:
        user = session.query(RegisteredUser).filter_by(username=username_input).first()
        if user and password_input is not None:
            if check_password_hash(user.password, password_input):
                return ""
            else:
                return "Incorrect password"
        elif user is None:
            return "Incorrect username"
    else:
        return ""
