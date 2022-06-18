import dash
import dash_bootstrap_components as dbc
from flask_login import LoginManager
import yaml
import os
import sys
from models_items.models import get_session, RegisteredUser

# load config file
cfg = yaml.safe_load(open("config.yaml"))

# dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(dir))

session = get_session()
engine = session.get_bind()

# bootstrap theme
# https://bootswatch.com/lux/
external_stylesheets = [dbc.themes.LUX]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True

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


# if __name__ == "__main__":
#     app.run_server(debug=True)
