from dash import dcc, html
from dash.dependencies import Input, Output, State
from models_items.models import RegisteredUser
from werkzeug.security import generate_password_hash
from app import session, app


def serve_layout() -> html.Div:
    return html.Div(
        [
            html.H1("Create User Account"),
            dcc.Location(id="create_user", refresh=True),
            dcc.Input(
                id="username", type="text", placeholder="user name", maxLength=15
            ),
            dcc.Input(id="password", type="password", placeholder="password"),
            html.Button("Create User", id="submit-val", n_clicks=0),
            html.Div(children="", id="container-button-basic"),
        ],
        style={"display": "flex", "justifyContent": "center"},
    )


@app.callback(
    Output("container-button-basic", "children"),
    [Input("submit-val", "n_clicks")],
    [
        State("username", "value"),
        State("password", "value"),
    ],
)
def insert_user(n_clicks, uname, pw):
    if uname is not None and pw is not None:
        hashed_password = generate_password_hash(pw, method="sha256")
        user = RegisteredUser(username=uname, password=hashed_password)
        session.add(user)
        session.commit()
        session.close()
        return f"User {uname} created successfully"
    else:
        return ""

    # else:
    #     return [
    #         html.Div(
    #             [
    #                 html.H2("Already have a user account?"),
    #                 dcc.Link("Click here to Log In", href="/login"),
    #             ],
    #             style={
    #                 "display": "inline-block",
    #                 "verticalAlign": "top",
    #                 "margin-top": "10",
    #             },
    #         ),
    #     ]
