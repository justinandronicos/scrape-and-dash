from datetime import date
import dash
import numpy
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
from dash import dash_table
from sqlalchemy.orm import session
import yaml
import sys
import os
from sqlalchemy import create_engine, select, join, cast, Date

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

from utilities import get_session
from models import (
    FFBrand,
    FFCurrentPrice,
    FFHistoricalPrice,
    FFProduct,
    GMBrand,
    GMCurrentPrice,
    GMHistoricalPrice,
    GMProduct,
    NLBrand,
    NLCurrentPrice,
    NLHistoricalPrice,
    NLProduct,
    WMBrand,
    WMCurrentPrice,
    WMHistoricalPrice,
    WMProduct,
)

cfg = yaml.safe_load(open("config.yaml"))

session = get_session()
engine = create_engine(cfg["db_connection_string"], echo=True)
# connection = engine.connect()

app = dash.Dash(__name__)

# website_tables = {
#     "nl": (NLProduct, NLBrand, NLCurrentPrice, NLHistoricalPrice),
#     "ff": (FFProduct, FFBrand, FFCurrentPrice, FFHistoricalPrice),
#     "gm": (GMProduct, GMBrand, GMCurrentPrice, GMHistoricalPrice),
#     "wm": (WMProduct, WMBrand, WMCurrentPrice, WMHistoricalPrice),
# }

# websites_dict = cfg["website_names"]

nl_stmt = (
    session.query(
        NLProduct.code,
        NLProduct.name,
        # NLProduct.variant,
        NLBrand.name.label("brand_name"),
        NLCurrentPrice.retail_price,
        NLCurrentPrice.time_stamp.cast(Date),  # Converted from datetime to date
        NLCurrentPrice.on_sale,
        NLCurrentPrice.current_price,
        NLCurrentPrice.in_stock,
        NLHistoricalPrice.retail_price.label("historical_retail_price"),
        NLHistoricalPrice.time_stamp.label("historical_time_stamp").cast(
            Date
        ),  # Converted from datetime to date
        NLHistoricalPrice.on_sale.label("historical_on_sale"),
        NLHistoricalPrice.current_price.label("historical_current_price"),
        NLHistoricalPrice.in_stock.label("historical_in_stock"),
        NLProduct.url,
    )
    .join(NLBrand, NLBrand.id == NLProduct.brand_id)
    .join(NLCurrentPrice, NLCurrentPrice.product_id == NLProduct.id)
    .join(NLHistoricalPrice, NLHistoricalPrice.product_id == NLProduct.id)
    .order_by(NLProduct.name)
).statement

nl_df = pd.read_sql(nl_stmt, con=engine)


ff_stmt = (
    session.query(
        FFProduct.code,
        FFProduct.name,
        # FFProduct.variant,
        FFBrand.name.label("brand_name"),
        FFCurrentPrice.retail_price,
        FFCurrentPrice.time_stamp.cast(Date),  # Converted from datetime to date
        FFCurrentPrice.on_sale,
        FFCurrentPrice.current_price,
        FFCurrentPrice.in_stock,
        FFHistoricalPrice.retail_price.label("historical_retail_price"),
        FFHistoricalPrice.time_stamp.label("historical_time_stamp").cast(
            Date
        ),  # Converted from datetime to date
        FFHistoricalPrice.on_sale.label("historical_on_sale"),
        FFHistoricalPrice.current_price.label("historical_current_price"),
        FFHistoricalPrice.in_stock.label("historical_in_stock"),
        FFProduct.url,
    )
    .join(FFBrand, FFBrand.id == FFProduct.brand_id)
    .join(FFCurrentPrice, FFCurrentPrice.product_id == FFProduct.id)
    .join(FFHistoricalPrice, FFHistoricalPrice.product_id == FFProduct.id)
    .order_by(FFProduct.name)
).statement

ff_df = pd.read_sql(ff_stmt, con=engine)


gm_stmt = (
    session.query(
        GMProduct.code,
        GMProduct.name,
        # GMProduct.variant,
        GMBrand.name.label("brand_name"),
        GMCurrentPrice.retail_price,
        GMCurrentPrice.time_stamp.cast(Date),  # Converted from datetime to date
        GMCurrentPrice.on_sale,
        GMCurrentPrice.current_price,
        GMCurrentPrice.in_stock,
        GMHistoricalPrice.retail_price.label("historical_retail_price"),
        GMHistoricalPrice.time_stamp.label("historical_time_stamp").cast(
            Date
        ),  # Converted from datetime to date
        GMHistoricalPrice.on_sale.label("historical_on_sale"),
        GMHistoricalPrice.current_price.label("historical_current_price"),
        GMHistoricalPrice.in_stock.label("historical_in_stock"),
        GMProduct.url,
    )
    .join(GMBrand, GMBrand.id == GMProduct.brand_id)
    .join(GMCurrentPrice, GMCurrentPrice.product_id == GMProduct.id)
    .join(GMHistoricalPrice, GMHistoricalPrice.product_id == GMProduct.id)
    .order_by(GMProduct.name)
).statement

gm_df = pd.read_sql(gm_stmt, con=engine)


wm_stmt = (
    session.query(
        WMProduct.code,
        WMProduct.name,
        # WMProduct.variant,
        WMBrand.name.label("brand_name"),
        WMCurrentPrice.retail_price,
        WMCurrentPrice.time_stamp.cast(Date),  # Converted from datetime to date
        WMCurrentPrice.on_sale,
        WMCurrentPrice.current_price,
        WMCurrentPrice.in_stock,
        WMHistoricalPrice.retail_price.label("historical_retail_price"),
        WMHistoricalPrice.time_stamp.label("historical_time_stamp").cast(
            Date
        ),  # Converted from datetime to date
        WMHistoricalPrice.on_sale.label("historical_on_sale"),
        WMHistoricalPrice.current_price.label("historical_current_price"),
        WMHistoricalPrice.in_stock.label("historical_in_stock"),
        WMProduct.url,
    )
    .join(WMBrand, WMBrand.id == WMProduct.brand_id)
    .join(WMCurrentPrice, WMCurrentPrice.product_id == WMProduct.id)
    .join(WMHistoricalPrice, WMHistoricalPrice.product_id == WMProduct.id)
    .order_by(WMProduct.name)
).statement

wm_df = pd.read_sql(wm_stmt, con=engine)


brand_dict = {
    "nl": sorted(nl_df["brand_name"].unique()),
    "ff": sorted(ff_df["brand_name"].unique()),
    "gm": sorted(gm_df["brand_name"].unique()),
    "wm": sorted(wm_df["brand_name"].unique()),
}

# dates_dict = {
#     "nl": [
#         numpy.unique(
#             numpy.append(
#                 nl_df["historical_time_stamp"].unique(), nl_df["time_stamp"].unique()
#             )
#         )[::-1].sort()
#     ],
#     "ff": [
#         {"label": i, "value": i}
#         for i in numpy.append(
#             ff_df["historical_time_stamp"].unique(), ff_df["time_stamp"].unique()
#         )
#     ],
#     "gm": [
#         {"label": i, "value": i}
#         for i in numpy.append(
#             gm_df["historical_time_stamp"].unique(), gm_df["time_stamp"].unique()
#         )
#     ],
#     "wm": [
#         {"label": i, "value": i}
#         for i in numpy.append(
#             wm_df["historical_time_stamp"].unique(), wm_df["time_stamp"].unique()
#         )
#     ],
# }

# nl_dates = numpy.append(
#     nl_df["historical_time_stamp"].unique(), nl_df["time_stamp"].unique()
# )
# ff_dates = numpy.append(
#     ff_df["historical_time_stamp"].unique(), ff_df["time_stamp"].unique()
# )
# gm_dates = numpy.append(
#     gm_df["historical_time_stamp"].unique(), gm_df["time_stamp"].unique()
# )
# wm_dates = numpy.append(
#     wm_df["historical_time_stamp"].unique(), wm_df["time_stamp"].unique()
# )
dates_dict = {
    "nl": [
        numpy.append(
            nl_df["historical_time_stamp"].unique(), nl_df["time_stamp"].unique()
        )
    ],
    "ff": [
        numpy.append(
            ff_df["historical_time_stamp"].unique(), ff_df["time_stamp"].unique()
        )
    ],
    "gm": [
        numpy.append(
            gm_df["historical_time_stamp"].unique(), gm_df["time_stamp"].unique()
        )
    ],
    "wm": [
        numpy.append(
            wm_df["historical_time_stamp"].unique(), wm_df["time_stamp"].unique()
        )
    ],
}


# print(f"\n\n FF HIST DATES: {ff_df['historical_time_stamp'].unique()}")
# print(f"\n\n FF CUR DATES: {ff_df['time_stamp'].unique()}")


# print(f"\n\n NL DATE: {dates_dict['nl']}")
# print(f"\n\n FF DATE: {dates_dict['ff']}")

# print(f"\n\n WM HIST DATES: {wm_df['historical_time_stamp'].unique()}")
# print(f"\n\n WM CUR DATES: {wm_df['time_stamp'].unique()}")

# print(f"\n\n WM DATE: {dates_dict['wm']}")

# print(f"\n\n WM DF : {wm_df}")

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
                    style={"width": "25%", "textAlign": "center"},
                ),
                html.Div(
                    [
                        "Date",
                        dcc.Dropdown(
                            id="date-dropdown",
                            # value="latest",
                            value="latest",
                            clearable=False,
                        ),
                        html.Div(id="date-dd-output-container"),
                    ],
                    style={"width": "25%", "textAlign": "center"},
                ),
                html.Div(
                    [
                        "Brand",
                        dcc.Dropdown(
                            id="brand-dropdown",
                            placeholder="Select Brand...",
                        ),
                        html.Div(id="brand-dd-output-container"),
                    ],
                    style={"width": "25%", "textAlign": "center"},
                ),
                html.Div(
                    [
                        html.Button("Download CSV", id="btn_csv"),
                        dcc.Download(id="download-datatable-csv"),
                    ],
                    style={"width": "10%"},
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
    # Output("date-dropdown", "value"),
    Output("date-dropdown", "options"),
    Output("date-dropdown", "value"),
    Input("website-dropdown", "value"),
)
def update_date_options_value(selected_website):
    """Updates date options after website selected and sets selected date to latest available by default"""

    date_array = numpy.unique(dates_dict[selected_website])
    date_array[::-1].sort()  # Sort dates descending
    # print(date_array)
    # print(f"\n\n {[{'label': i, 'value': i} for i in date_array]}")
    return [{"label": i, "value": i} for i in date_array], date_array[0]
    # website_df = (
    #     nl_df
    #     if selected_website == "nl"
    #     else ff_df
    #     if selected_website == "ff"
    #     else gm_df
    #     if selected_website == "gm"
    #     else wm_df
    #     if selected_website == "wm"
    #     else None
    # )

    # print(f"\n\n UNIQUE1: {website_df['time_stamp'].unique()}")
    # print(f"\n\n UNIQUE2: {website_df['historical_time_stamp'].unique()}")
    # date_array = numpy.unique(
    #     numpy.append(
    #         website_df["historical_time_stamp"].unique(),
    #         website_df["time_stamp"].unique(),
    #     )
    # )
    # date_array[::-1].sort()  # Sort dates descending
    # # sorted_dates = sorted(date_array.tolist())
    # print(date_array)
    # print(f"\n\n {[{'label': i, 'value': i} for i in date_array]}")
    # return [{"label": i, "value": i} for i in date_array]


@app.callback(
    Output("brand-dropdown", "options"),
    Input("website-dropdown", "value"),
)
def update_brand_options(selected_brand):
    return [{"label": i, "value": i} for i in brand_dict[selected_brand]]


# @app.callback(
#     Output("table", "data"),
#     Output("table", "columns"),
#     Input("website-dropdown", "value"),
#     Input("brand-dropdown", "value"),
# )
def filter_table_by_brand(df, selected_brand):
    filtered_df = df.loc[df["brand_name"] == selected_brand]
    return filtered_df.drop("brand_name", axis=1, inplace=False)
    #     nl_df
    #     if selected_website == "nl"
    #     else ff_df
    #     if selected_website == "ff"
    #     else gm_df
    #     if selected_website == "gm"
    #     else wm_df
    #     if selected_website == "wm"
    #     else None
    # )
    # filtered_df = website_df.loc[website_df["brand_name"] == selected_brand]
    # columns = [{"name": i, "id": i} for i in filtered_df.columns]
    # return filtered_df.to_dict("records"), columns


def filter_table_by_date(website_df, selected_date, date_options):
    dates = [x["value"] for x in date_options]
    # print(f"\n\n Sorted: {dates}")
    # print(f"\n\n Selected: {selected_date}")
    # print(f"\n\n df: {website_df}")
    formatted_date = date.fromisoformat(selected_date)
    # print(f"DATE: {str(formatted_date)}")
    # print(f"DATE: {dates[0]}")
    if selected_date == dates[0] or selected_date == "latest":
        filtered_df = website_df.drop(
            [
                "historical_retail_price",
                "historical_time_stamp",
                "historical_on_sale",
                "historical_current_price",
                "historical_in_stock",
            ],
            axis=1,
            inplace=False,
        )
        filtered_df = filtered_df.drop_duplicates()
    else:
        filtered_df = website_df.drop(
            ["retail_price", "time_stamp", "on_sale", "current_price", "in_stock"],
            axis=1,
            inplace=False,
        )
        # print(f"\n\n filtered df: {filtered_df}")
        filtered_df = filtered_df.loc[
            filtered_df["historical_time_stamp"] == date.fromisoformat(selected_date)
        ]
        # print(f"\n\n refiltered df: {filtered_df}")
    return filtered_df


@app.callback(
    Output("table", "data"),
    Output("table", "columns"),
    Input("website-dropdown", "value"),
    Input("date-dropdown", "value"),
    Input("date-dropdown", "options"),
    Input("brand-dropdown", "value"),
)
def update_table(selected_website, selected_date, date_options, selected_brand):
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

    # ids = website_df.loc[website_df["code"] == "2597686/1"]
    # print(f"\n\n IDs: {ids['time_stamp']} , {ids['historical_time_stamp']}")

    filtered_df = filter_table_by_date(website_df, selected_date, date_options)

    if selected_brand is not None:
        filtered_df = filter_table_by_brand(filtered_df, selected_brand)

    columns = [{"name": i, "id": i} for i in filtered_df.columns]
    return filtered_df.to_dict("records"), columns


@app.callback(
    Output("download-datatable-csv", "data"),
    Input("btn_csv", "n_clicks"),
    State("table", "data"),
    State("website-dropdown", "value"),
    State("date-dropdown", "value"),
    State("brand-dropdown", "value"),
    prevent_initial_call=True,
)
def download_table(n_clicks, data, selected_website, selected_date, selected_brand):
    df = pd.DataFrame.from_records(data)
    if selected_brand is not None:
        filename = f"{cfg['website_names'][selected_website]}_{selected_brand}_{selected_date}_products_prices.csv"
    else:
        filename = f"{cfg['website_names'][selected_website]}_{selected_date}_products_prices.csv"
    return dcc.send_data_frame(
        df.to_csv,
        filename=filename,
        index=False,
    )


if __name__ == "__main__":
    app.run_server(debug=True)

# TODO: Search box, date dropdown (unique dates from cached query results for brand)
# Callback to get all results for brand on page load


# @retry(wait=wait_exponential(multiplier=2, min=1, max=10), stop=stop_after_attempt(5))
# def try_connection():
#     try:
#         with postgres_engine.connect() as connection:
#             stmt = text("SELECT 1")
#             connection.execute(stmt)
#         print("Connection to database successful.")

#     except Exception as e:
#         print("Connection to database failed, retrying.")
#         raise Exception


# app.layout = html.Div(
#     [
#         dcc.Graph(id="graph-with-slider"),
#         dcc.Slider(
#             id="year-slider",
#             min=df["year"].min(),
#             max=df["year"].max(),
#             value=df["year"].min(),
#             marks={str(year): str(year) for year in df["year"].unique()},
#             step=None,
#         ),
#     ]
# )


# @app.callback(Output("graph-with-slider", "figure"), Input("year-slider", "value"))
# def update_figure(selected_year):
#     filtered_df = df[df.year == selected_year]

#     fig = px.scatter(
#         filtered_df,
#         x="gdpPercap",
#         y="lifeExp",
#         size="pop",
#         color="continent",
#         hover_name="country",
#         log_x=True,
#         size_max=55,
#     )

#     fig.update_layout(transition_duration=500)

#     return fig


# nl_df = pd.read_sql(
#     session.query(NLProduct)
#     .join(NLBrand.name)
#     .join(
#         NLCurrentPrice.retail_price,
#         NLCurrentPrice.time_stamp,
#         NLCurrentPrice.on_sale,
#         NLCurrentPrice.current_price,
#         NLCurrentPrice.in_stock,
#     )
#     .join(
#         NLHistoricalPrice.retail_price,
#         NLHistoricalPrice.time_stamp,
#         NLHistoricalPrice.on_sale,
#         NLHistoricalPrice.current_price,
#         NLHistoricalPrice.in_stock,
#     )
#     .statement,
#     con=engine,
# )
# ff_df = pd.read_sql(
#     session.query(FFProduct)
#     .join(FFBrand.name)
#     .join(
#         FFCurrentPrice.retail_price,
#         FFCurrentPrice.time_stamp,
#         FFCurrentPrice.on_sale,
#         FFCurrentPrice.current_price,
#         FFCurrentPrice.in_stock,
#     )
#     .join(
#         FFHistoricalPrice.retail_price,
#         FFHistoricalPrice.time_stamp,
#         FFHistoricalPrice.on_sale,
#         FFHistoricalPrice.current_price,
#         FFHistoricalPrice.in_stock,
#     )
#     .statement,
#     con=engine,
# )
# gm_df = pd.read_sql(
#     session.query(GMProduct)
#     .join(GMBrand.name)
#     .join(
#         GMCurrentPrice.retail_price,
#         GMCurrentPrice.time_stamp,
#         GMCurrentPrice.on_sale,
#         GMCurrentPrice.current_price,
#         GMCurrentPrice.in_stock,
#     )
#     .join(
#         GMHistoricalPrice.retail_price,
#         GMHistoricalPrice.time_stamp,
#         GMHistoricalPrice.on_sale,
#         GMHistoricalPrice.current_price,
#         GMHistoricalPrice.in_stock,
#     )
#     .statement,
#     con=engine,
# )
# wm_df = pd.read_sql(
#     session.query(WMProduct)
#     .join(WMBrand.name)
#     .join(
#         WMCurrentPrice.retail_price,
#         WMCurrentPrice.time_stamp,
#         WMCurrentPrice.on_sale,
#         WMCurrentPrice.current_price,
#         WMCurrentPrice.in_stock,
#     )
#     .join(
#         WMHistoricalPrice.retail_price,
#         WMHistoricalPrice.time_stamp,
#         WMHistoricalPrice.on_sale,
#         WMHistoricalPrice.current_price,
#         WMHistoricalPrice.in_stock,
#     )
#     .statement,
#     con=engine,
# )
