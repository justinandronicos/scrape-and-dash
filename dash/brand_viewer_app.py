import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
from dash import dash_table
from sqlalchemy.orm import session
import yaml
import sys
import os
from sqlalchemy import create_engine, func

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

from utilities import get_session
from models import (
    FFBrand,
    GMBrand,
    NLBrand,
    WMBrand,
    FFProduct,
    GMProduct,
    NLProduct,
    WMProduct,
)

cfg = yaml.safe_load(open("config.yaml"))

session = get_session()
engine = create_engine(cfg["db_connection_string"], echo=True)
# connection = engine.connect()

app = dash.Dash(__name__)

nl_stmt = (
    session.query(
        NLBrand.name.label("brand_name"),
        func.count(NLProduct.brand_id).label("product_count"),
        NLBrand.url.label("url"),
    )
    .join(NLBrand, NLBrand.id == NLProduct.brand_id)
    .group_by(NLBrand.name, NLBrand.url)
    .order_by(NLBrand.name)
).statement
nl_df = pd.read_sql(nl_stmt, con=engine)

print(f"\n\n\n NF: {nl_df}")

ff_stmt = (
    session.query(
        FFBrand.name.label("brand_name"),
        func.count(FFProduct.brand_id).label("product_count"),
        FFBrand.url.label("url"),
    )
    .join(FFBrand, FFBrand.id == FFProduct.brand_id)
    .group_by(FFBrand.name, FFBrand.url)
    .order_by(FFBrand.name)
).statement
ff_df = pd.read_sql(ff_stmt, con=engine)

print(f"\n\n\n FF: {ff_df}")

gm_stmt = (
    session.query(
        GMBrand.name.label("brand_name"),
        func.count(GMProduct.brand_id).label("product_count"),
        GMBrand.url.label("url"),
    )
    .join(GMBrand, GMBrand.id == GMProduct.brand_id)
    .group_by(GMBrand.name, GMBrand.url)
    .order_by(GMBrand.name)
).statement
gm_df = pd.read_sql(gm_stmt, con=engine)

print(f"\n\n\n GM: {gm_df}")

wm_stmt = (
    session.query(
        WMBrand.name.label("brand_name"),
        func.count(WMProduct.brand_id).label("product_count"),
        WMBrand.url.label("url"),
    )
    .join(WMBrand, WMBrand.id == WMProduct.brand_id)
    .group_by(WMBrand.name, WMBrand.url)
    .order_by(WMBrand.name)
).statement
wm_df = pd.read_sql(wm_stmt, con=engine)

print(f"\n\n\n WM: {wm_df}")

app.layout = html.Div(
    [
        html.Div(
            className="filters_row",
            children=[
                html.Div(
                    [
                        "Website",
                        dcc.Dropdown(
                            id="website-dropdown",
                            options=[
                                {"label": cfg["website_names"]["nl"], "value": "nl"},
                                {"label": cfg["website_names"]["ff"], "value": "ff"},
                                {"label": cfg["website_names"]["gm"], "value": "gm"},
                                {"label": cfg["website_names"]["wm"], "value": "wm"},
                            ],
                            value="nl",
                            clearable=False,
                        ),
                        html.Div(id="website-dd-output-container"),
                    ],
                    style={"width": "30%", "textAlign": "center"},
                ),
                html.Div(
                    [
                        "Number of Brands: ",
                        dash.html.Output(
                            id="brand_count_output", children=str(len(nl_df))
                        ),
                        html.Div(id="brand-count-output-container"),
                    ],
                    style={
                        "width": "20%",
                        "textAlign": "center",
                    },
                ),
                html.Div(
                    [
                        html.Button("Download CSV", id="btn_csv"),
                        dcc.Download(id="download-datatable-csv"),
                        html.Div(id="download-btn-container"),
                    ],
                    style={"width": "20%"},
                ),
            ],
            style=dict(display="flex", horizontalAlign="center"),
        ),
        html.Div(
            [
                dash_table.DataTable(
                    id="table",
                    columns=[{"name": i, "id": i} for i in nl_df.columns],
                    data=nl_df.to_dict("records"),
                )
            ]
        ),
    ]
)


@app.callback(
    Output("brand_count_output", "children"),
    Input("website-dropdown", "value"),
)
def update_brand_count(selected_website):
    brand_count = (
        len(nl_df)
        if selected_website == "nl"
        else len(ff_df)
        if selected_website == "ff"
        else len(gm_df)
        if selected_website == "gm"
        else len(wm_df)
        if selected_website == "wm"
        else None
    )
    return str(brand_count)


@app.callback(
    Output("table", "data"),
    Output("table", "columns"),
    Input("website-dropdown", "value"),
)
def update_table(selected_website):
    website_df = (
        nl_df
        if selected_website == "nl"
        else ff_df
        if selected_website == "ff"
        else gm_df
        if selected_website == "gm"
        else wm_df
        if selected_website == "wm"
        else None
    )

    columns = [{"name": i, "id": i} for i in website_df.columns]
    return website_df.to_dict("records"), columns


@app.callback(
    Output("download-datatable-csv", "data"),
    Input("btn_csv", "n_clicks"),
    State("table", "data"),
    State("website-dropdown", "value"),
    prevent_initial_call=True,
)
def download_table(n_clicks, data, selected_website):
    df = pd.DataFrame.from_records(data)
    filename = f"{cfg['website_names'][selected_website]}_brands_list.csv"
    return dcc.send_data_frame(
        df.to_csv,
        filename=filename,
        index=False,
    )


if __name__ == "__main__":
    app.run_server(debug=True)
