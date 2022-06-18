from dash import dcc, html, no_update
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from importlib import import_module
from flask_login import logout_user, current_user

# from sqlalchemy.orm.base import PASSIVE_NO_FETCH
from app import app

# Import all pages in the app
from pages import (
    best_selling_viewer,
    brand_viewer,
    compare_by_brand,
    highest_rated_viewer,
    products_viewer,
    home,
    file_upload,
    create_user,
    login,
    logout,
)

# Building the navigation bar
# https://github.com/facultyai/dash-bootstrap-components/blob/master/examples/advanced-component-usage/Navbars.py
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Home", href="/"),
        dbc.DropdownMenuItem("View Products", href="/products"),
        dbc.DropdownMenuItem("View Brands", href="/brands"),
        dbc.DropdownMenuItem("Compare by Brand", href="/brand-comparison"),
        dbc.DropdownMenuItem("Best Selling", href="/best-selling"),
        dbc.DropdownMenuItem("Highest Rated", href="/highest-rated"),
        dbc.DropdownMenuItem("Upload Product File", href="/file-upload"),
    ],
    nav=True,
    in_navbar=True,
    label="Explore",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/data_table.png", height="30px")),
                        dbc.Col(
                            dbc.NavbarBrand("Project Scrape and DASH", className="ml-2")
                        ),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    # Right align dropdown menu with ml-auto className
                    [dropdown],
                    className="ml-auto",
                    navbar=True,
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.A("Create User", href="/create-user", className="ml-2"),
                        id="create-user-link",
                    ),
                    dbc.Col(
                        html.A("Logout", href="/logout", className="ml-2"),
                        id="logout-link",
                    ),
                ],
                align="center",
                className="g-0",
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-4",
)


def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

# Embedding the navigation bar
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), navbar, html.Div(id="page-content")]
)

# "Complete" layout
app.validation_layout = html.Div(
    [
        import_module("pages." + appname).serve_layout()
        for appname in [
            "best_selling_viewer",
            "brand_viewer",
            "compare_by_brand",
            "highest_rated_viewer",
            "products_viewer",
            "file_upload",
            "home",
            "create_user",
            "login",
            "logout",
        ]
    ]
)


@app.callback(
    Output("logout-link", "style"),
    Output("create-user-link", "style"),
    Input("url", "pathname"),
)
def show_hide_links(pathname):
    """Dynamically shows or hides logout and create user links in navbar based on whether
    user is logged in"""
    if current_user.is_authenticated and pathname != "/logout":
        return {"display": "inline-block"}, {"display": "inline-block"}
    else:
        return {"display": "none"}, {"display": "none"}


@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def display_page(pathname):
    """Handles layout display/routing with authentication check"""
    if current_user.is_authenticated:
        if pathname == "/products":
            return products_viewer.serve_layout()
        elif pathname == "/brands":
            return brand_viewer.serve_layout()
        elif pathname == "/brand-comparison":
            return compare_by_brand.serve_layout()
        elif pathname == "/best-selling":
            return best_selling_viewer.serve_layout()
        elif pathname == "/highest-rated":
            return highest_rated_viewer.serve_layout()
        elif pathname == "/file-upload":
            return file_upload.serve_layout()
        elif pathname == "/file-upload":
            return file_upload.serve_layout()
        elif pathname == "/create-user":
            return create_user.serve_layout()
        elif pathname == "/logout":
            logout_user()
            return logout.serve_layout()
        elif pathname == "/" or pathname == "/home":
            return home.serve_layout()
        else:
            return "404"
    else:
        return login.serve_layout()

    # else:
    # if pathname == "/create":
    #     return create_user.layout
    # else:
    # return login.layout


# @app.callback(
#     Output("url", "pathname"),
#     Input("url", "pathname"),
#     # State("url", "pathname"),
# )
# def display_login(content):
#     if current_user.is_authenticated:
#         return no_update
#     else:
#         return "/login"


if __name__ == "__main__":
    ## Docker Local
    # app.run_server(debug=True, host="0.0.0.0", port=8080)
    ## Local
    app.run_server(debug=True, host="127.0.0.1", port=8050)
