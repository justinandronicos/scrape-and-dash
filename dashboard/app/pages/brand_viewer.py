import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
from dash import dash_table
from sqlalchemy import func, select

from models_items.models import (
    FFBrand,
    GMBrand,
    NLBrand,
    WMBrand,
    FFProduct,
    GMProduct,
    NLProduct,
    WMProduct,
)
from app import app, session, engine, cfg

website_names = cfg["website_names"]

nl_stmt = (
    select(
        NLBrand.name.label("brand_name"),
        func.count(NLProduct.brand_id).label("product_count"),
        NLBrand.url.label("url"),
    )
    .join(NLBrand, NLBrand.id == NLProduct.brand_id)
    .group_by(NLBrand.name, NLBrand.url)
)
nl_df = pd.read_sql(nl_stmt, con=engine)


ff_stmt = (
    select(
        FFBrand.name.label("brand_name"),
        func.count(FFProduct.brand_id).label("product_count"),
        FFBrand.url.label("url"),
    )
    .join(FFBrand, FFBrand.id == FFProduct.brand_id)
    .group_by(FFBrand.name, FFBrand.url)
)
ff_df = pd.read_sql(ff_stmt, con=engine)

gm_stmt = (
    select(
        GMBrand.name.label("brand_name"),
        func.count(GMProduct.brand_id).label("product_count"),
        GMBrand.url.label("url"),
    )
    .join(GMBrand, GMBrand.id == GMProduct.brand_id)
    .group_by(GMBrand.name, GMBrand.url)
)
gm_df = pd.read_sql(gm_stmt, con=engine)


wm_stmt = (
    select(
        WMBrand.name.label("brand_name"),
        func.count(WMProduct.brand_id).label("product_count"),
        WMBrand.url.label("url"),
    )
    .join(WMBrand, WMBrand.id == WMProduct.brand_id)
    .group_by(WMBrand.name, WMBrand.url)
)
wm_df = pd.read_sql(wm_stmt, con=engine)


def serve_layout() -> html.Div:
    return html.Div(
        [
            html.Div(html.H2("Brands Viewer"), style={"textAlign": "center"}),
            html.Div(
                className="bv-filters-row",
                children=[
                    html.Div(
                        [
                            html.B("Website"),
                            dcc.Dropdown(
                                id="bv-website-dropdown",
                                options=[
                                    {"label": website_names["nl"], "value": "nl"},
                                    {"label": website_names["ff"], "value": "ff"},
                                    {"label": website_names["gm"], "value": "gm"},
                                    {"label": website_names["wm"], "value": "wm"},
                                ],
                                value="nl",
                                clearable=False,
                            ),
                            # html.Div(id="website-dd-output-container"),
                        ],
                        style={"width": "30%", "textAlign": "center"},
                    ),
                    html.Div(
                        [
                            html.B("Sort By"),
                            dcc.Dropdown(
                                id="bv-sort-dropdown",
                                options=[
                                    {"label": "Brand Name", "value": "brand_name"},
                                    {"label": "Product Count", "value": "prod_count"},
                                ],
                                value="brand_name",
                                clearable=False,
                            ),
                            # html.Div(id="sort-dd-output-container"),
                        ],
                        style={"width": "30%", "textAlign": "center"},
                    ),
                    html.Div(
                        [
                            "Number of Brands: ",
                            dash.html.Output(
                                id="bv-brand-count-output", children=str(len(nl_df))
                            ),
                            # html.Div(id="brand-count-output-container"),
                        ],
                        style={
                            "width": "20%",
                            "textAlign": "center",
                        },
                    ),
                    html.Div(
                        [
                            html.Button("Download CSV", id="bv-btn-csv"),
                            dcc.Download(id="bv-download-datatable-csv"),
                            # html.Div(id="download-btn-container"),
                        ],
                        style={"width": "20%"},
                    ),
                ],
                style={"display": "flex", "horizontalAlign": "center"},
            ),
            html.Div(
                [
                    dash_table.DataTable(
                        id="bv-table",
                        columns=[{"name": i, "id": i} for i in nl_df.columns],
                        data=nl_df.to_dict("records"),
                    )
                ]
            ),
        ]
    )


@app.callback(
    Output("bv-brand-count-output", "children"),
    Input("bv-website-dropdown", "value"),
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
    Output("bv-table", "data"),
    Output("bv-table", "columns"),
    Input("bv-website-dropdown", "value"),
    Input("bv-sort-dropdown", "value"),
)
def update_table(selected_website, sort_by):
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
    if sort_by == "brand_name":
        sorted_df = website_df.sort_values(by="brand_name", ascending=True)
    else:
        sorted_df = website_df.sort_values(by="product_count", ascending=False)

    columns = [{"name": i, "id": i} for i in sorted_df.columns]
    return sorted_df.to_dict("records"), columns


@app.callback(
    Output("bv-download-datatable-csv", "data"),
    Input("bv-btn-csv", "n_clicks"),
    State("bv-table", "data"),
    State("bv-website-dropdown", "value"),
    prevent_initial_call=True,
)
def download_table(n_clicks, data, selected_website):
    df = pd.DataFrame.from_records(data)
    filename = f"{website_names[selected_website]}_brands_list.csv"
    return dcc.send_data_frame(
        df.to_csv,
        filename=filename,
        index=False,
    )
