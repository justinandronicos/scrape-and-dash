from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from importlib import import_module

from app import app

# Import all pages in the app
from apps import (
    best_selling_viewer,
    brand_viewer,
    compare_by_brand,
    highest_rated_viewer,
    products_viewer,
    home,
    file_upload,
)

# Building the navigation bar
# https://github.com/facultyai/dash-bootstrap-components/blob/master/examples/advanced-component-usage/Navbars.py
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Home", href="/home"),
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
                href="/home",
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
        import_module("apps." + appname).layout
        for appname in [
            "best_selling_viewer",
            "brand_viewer",
            "compare_by_brand",
            "highest_rated_viewer",
            "products_viewer",
            "file_upload"
        ]
    ]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/products":
        return products_viewer.layout
    elif pathname == "/brands":
        return brand_viewer.layout
    elif pathname == "/brand-comparison":
        return compare_by_brand.layout
    elif pathname == "/best-selling":
        return best_selling_viewer.layout
    elif pathname == "/highest-rated":
        return highest_rated_viewer.layout
    elif pathname == "/file-upload":
        return file_upload.layout
    else:
        return home.layout


if __name__ == "__main__":
    app.run_server(debug=True)
