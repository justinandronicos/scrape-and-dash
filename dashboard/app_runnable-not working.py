import dash_bootstrap_components as dbc
from flask_login import LoginManager
import yaml
import os
from models_items.models import get_session, RegisteredUser, Base
from dash import Dash, dcc, html, Input, Output, callback
from importlib import import_module

# import sys

# load config file
cfg = yaml.safe_load(open("config.yaml"))

# dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(dir))


session = get_session()
engine = session.get_bind()
Base.metadata.create_all(engine, checkfirst=True)

# bootstrap theme
# https://bootswatch.com/lux/
external_stylesheets = [dbc.themes.LUX]

app = Dash(__name__, external_stylesheets=external_stylesheets)

# app.config.suppress_callback_exceptions = True

# from dash_app import app

# app = dash.Dash(__name__)

server = app.server

# config the server to interact with the database
# Secret Key is used for user sessions
server.config.update(
    SECRET_KEY=os.urandom(16),
    SQLALCHEMY_DATABASE_URI=cfg["db_connection_string"],
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# Setup the LoginManager for the server
login_manager = LoginManager()
# This provides default implementations for the methods that Flask-Login expects user objects to have
login_manager.init_app(server)
login_manager.login_view = "/login"

# Callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return session.query(RegisteredUser).get(int(user_id))


import index

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


# Embedding the navigation bar
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), index.navbar, html.Div(id="page-content")]
)

# "Complete" layout
app.validation_layout = html.Div(
    [
        import_module("pages." + appname).layout
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
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def display_page(pathname):
    """Handles layout display/routing with authentication check"""
    if current_user.is_authenticated:
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
        elif pathname == "/file-upload":
            return file_upload.layout
        elif pathname == "/create-user":
            return create_user.layout
        elif pathname == "/logout":
            logout_user()
            return logout.layout
        elif pathname == "/" or pathname == "/home":
            return home.layout
        else:
            return "404"
    else:
        return login.layout


if __name__ == "__main__":
    app.run_server(debug=True)
