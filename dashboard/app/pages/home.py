from dash import html
import dash_bootstrap_components as dbc

# external_stylesheets = [dbc.themes.LUX]

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# from dash_app import app

layout = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.H1(
                                "Welcome to the Scrape & Dash dashboard",
                                className="text-center",
                            ),
                            className="mb-5 mt-5",
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.H5(
                                children="This dashboard contains product and pricing data from 4 different ecommerce websites",
                                className="text-center",
                            ),
                            className="mb-4",
                        )
                    ]
                ),
            ]
        )
    ]
)
