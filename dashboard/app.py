import dash
import dash_bootstrap_components as dbc

import os
import sys

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))
from models import get_session

session = get_session()
engine = session.get_bind()

# bootstrap theme
# https://bootswatch.com/lux/
external_stylesheets = [dbc.themes.LUX]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# from dash_app import app

# app = dash.Dash(__name__)

server = app.server
# app.config.suppress_callback_exceptions = True

# if __name__ == "__main__":
#     app.run_server(debug=True)
