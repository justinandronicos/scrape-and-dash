from datetime import date
import numpy as np
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
from dash import dash_table
from sqlalchemy import Date, select
from collections import Counter

from models_items.models import (
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
from app import session, engine, app, cfg

website_names = cfg["website_names"]

nl_stmt = (
    select(
        NLProduct.name,
        # NLProduct.variant,
        NLBrand.name.label("brand_name"),
        # NLCurrentPrice.retail_price,
        NLCurrentPrice.time_stamp.cast(Date),  # Converted from datetime to date
        # NLCurrentPrice.on_sale,
        NLCurrentPrice.current_price,
        # NLCurrentPrice.in_stock,
        # NLHistoricalPrice.retail_price.label("historical_retail_price"),
        NLHistoricalPrice.time_stamp.label("historical_time_stamp").cast(
            Date
        ),  # Converted from datetime to date
        # NLHistoricalPrice.on_sale.label("historical_on_sale"),
        NLHistoricalPrice.current_price.label("historical_current_price"),
        # NLHistoricalPrice.in_stock.label("historical_in_stock"),
        # NLProduct.url,
    )
    .join(NLBrand, NLBrand.id == NLProduct.brand_id)
    .join(NLCurrentPrice, NLCurrentPrice.product_id == NLProduct.id)
    .join(NLHistoricalPrice, NLHistoricalPrice.product_id == NLProduct.id)
    .order_by(NLProduct.name)
)

nl_df = pd.read_sql(nl_stmt, con=engine)


ff_stmt = (
    select(
        FFProduct.name,
        # FFProduct.variant,
        FFBrand.name.label("brand_name"),
        # FFCurrentPrice.retail_price,
        FFCurrentPrice.time_stamp.cast(Date),  # Converted from datetime to date
        # FFCurrentPrice.on_sale,
        FFCurrentPrice.current_price,
        # FFCurrentPrice.in_stock,
        # FFHistoricalPrice.retail_price.label("historical_retail_price"),
        FFHistoricalPrice.time_stamp.label("historical_time_stamp").cast(
            Date
        ),  # Converted from datetime to date
        # FFHistoricalPrice.on_sale.label("historical_on_sale"),
        FFHistoricalPrice.current_price.label("historical_current_price"),
        # FFHistoricalPrice.in_stock.label("historical_in_stock"),
        # FFProduct.url,
    )
    .join(FFBrand, FFBrand.id == FFProduct.brand_id)
    .join(FFCurrentPrice, FFCurrentPrice.product_id == FFProduct.id)
    .join(FFHistoricalPrice, FFHistoricalPrice.product_id == FFProduct.id)
    .order_by(FFProduct.name)
)

ff_df = pd.read_sql(ff_stmt, con=engine)


gm_stmt = (
    select(
        GMProduct.name,
        # GMProduct.variant,
        GMBrand.name.label("brand_name"),
        # GMCurrentPrice.retail_price,
        GMCurrentPrice.time_stamp.cast(Date),  # Converted from datetime to date
        # GMCurrentPrice.on_sale,
        GMCurrentPrice.current_price,
        # GMCurrentPrice.in_stock,
        # GMHistoricalPrice.retail_price.label("historical_retail_price"),
        GMHistoricalPrice.time_stamp.label("historical_time_stamp").cast(
            Date
        ),  # Converted from datetime to date
        # GMHistoricalPrice.on_sale.label("historical_on_sale"),
        GMHistoricalPrice.current_price.label("historical_current_price"),
        # GMHistoricalPrice.in_stock.label("historical_in_stock"),
        # GMProduct.url,
    )
    .join(GMBrand, GMBrand.id == GMProduct.brand_id)
    .join(GMCurrentPrice, GMCurrentPrice.product_id == GMProduct.id)
    .join(GMHistoricalPrice, GMHistoricalPrice.product_id == GMProduct.id)
    .order_by(GMProduct.name)
)

gm_df = pd.read_sql(gm_stmt, con=engine)


wm_stmt = (
    select(
        WMProduct.name,
        # WMProduct.variant,
        WMBrand.name.label("brand_name"),
        # WMCurrentPrice.retail_price,
        WMCurrentPrice.time_stamp.cast(Date),  # Converted from datetime to date
        # WMCurrentPrice.on_sale,
        WMCurrentPrice.current_price,
        # WMCurrentPrice.in_stock,
        # WMHistoricalPrice.retail_price.label("historical_retail_price"),
        WMHistoricalPrice.time_stamp.label("historical_time_stamp").cast(
            Date
        ),  # Converted from datetime to date
        # WMHistoricalPrice.on_sale.label("historical_on_sale"),
        WMHistoricalPrice.current_price.label("historical_current_price"),
        # WMHistoricalPrice.in_stock.label("historical_in_stock"),
        # WMProduct.url,
    )
    .join(WMBrand, WMBrand.id == WMProduct.brand_id)
    .join(WMCurrentPrice, WMCurrentPrice.product_id == WMProduct.id)
    .join(WMHistoricalPrice, WMHistoricalPrice.product_id == WMProduct.id)
    .order_by(WMProduct.name)
)

wm_df = pd.read_sql(wm_stmt, con=engine)

df_dict = {
    "nl": nl_df,
    "ff": ff_df,
    "gm": gm_df,
    "wm": wm_df,
}

brand_dict = {
    "nl": dict.fromkeys(np.sort(nl_df["brand_name"].unique())),
    "ff": dict.fromkeys(np.sort(ff_df["brand_name"].unique())),
    "gm": dict.fromkeys(np.sort(gm_df["brand_name"].unique())),
    "wm": dict.fromkeys(np.sort(wm_df["brand_name"].unique())),
}

# dates_dict = {
#     "nl": [
#         np.append(nl_df["historical_time_stamp"].unique(), nl_df["time_stamp"].unique())
#     ],
#     "ff": [
#         np.append(ff_df["historical_time_stamp"].unique(), ff_df["time_stamp"].unique())
#     ],
#     "gm": [
#         np.append(gm_df["historical_time_stamp"].unique(), gm_df["time_stamp"].unique())
#     ],
#     "wm": [
#         np.append(wm_df["historical_time_stamp"].unique(), wm_df["time_stamp"].unique())
#     ],
# }

# date_array = np.intersect1d(
#     dates_dict["nl"], dates_dict["ff"], dates_dict["gm"], dates_dict["wm"]
# )

# start = time.time()
# date_list = []
# date_list.append(
#     nl_df["historical_time_stamp"].unique().tolist() + nl_df["time_stamp"].to_list()
# )
# date_list.append(
#     ff_df["historical_time_stamp"].unique().tolist() + ff_df["time_stamp"].to_list()
# )
# date_list.append(
#     gm_df["historical_time_stamp"].unique().tolist() + gm_df["time_stamp"].to_list()
# )
# date_list.append(
#     wm_df["historical_time_stamp"].unique().tolist() + wm_df["time_stamp"].to_list()
# )

# end = time.time()
# print(f"\n\n full list Time: {end - start}")


# start = time.time()
# date_array = np.concatenate(
#     (
#         np.unique(
#             np.append(
#                 nl_df["historical_time_stamp"].unique(), nl_df["time_stamp"].unique()
#             )
#         ),
#         np.unique(
#             np.append(
#                 ff_df["historical_time_stamp"].unique(), ff_df["time_stamp"].unique()
#             )
#         ),
#         np.unique(
#             np.append(
#                 gm_df["historical_time_stamp"].unique(), gm_df["time_stamp"].unique()
#             )
#         ),
#         np.unique(
#             np.append(
#                 wm_df["historical_time_stamp"].unique(), wm_df["time_stamp"].unique()
#             )
#         ),
#     )
# )
# date_array[::-1].sort()

date_dict = {
    "nl": dict.fromkeys(
        sorted(
            (
                np.append(
                    nl_df["historical_time_stamp"].unique(),
                    nl_df["time_stamp"].unique(),
                )
            ),
            reverse=True,
        )
    ),
    "ff": dict.fromkeys(
        sorted(
            (
                np.append(
                    ff_df["historical_time_stamp"].unique(),
                    ff_df["time_stamp"].unique(),
                )
            ),
            reverse=True,
        )
    ),
    "gm": dict.fromkeys(
        sorted(
            (
                np.append(
                    gm_df["historical_time_stamp"].unique(),
                    gm_df["time_stamp"].unique(),
                )
            ),
            reverse=True,
        )
    ),
    "wm": dict.fromkeys(
        sorted(
            (
                np.append(
                    wm_df["historical_time_stamp"].unique(),
                    wm_df["time_stamp"].unique(),
                )
            ),
            reverse=True,
        )
    ),
}

# date_dict = {
#     "nl": sorted(
#         np.unique(
#             np.append(
#                 nl_df["historical_time_stamp"].unique(), nl_df["time_stamp"].unique()
#             )
#         ),
#         reverse=True,
#     ),
#     "ff": sorted(
#         np.unique(
#             np.append(
#                 ff_df["historical_time_stamp"].unique(), ff_df["time_stamp"].unique()
#             )
#         ),
#         reverse=True,
#     ),
#     "gm": sorted(
#         np.unique(
#             np.append(
#                 gm_df["historical_time_stamp"].unique(), gm_df["time_stamp"].unique()
#             )
#         ),
#         reverse=True,
#     ),
#     "wm": sorted(
#         np.unique(
#             np.append(
#                 wm_df["historical_time_stamp"].unique(), wm_df["time_stamp"].unique()
#             )
#         ),
#         reverse=True,
#     ),
# }


# end = time.time()
# print(f"\n\n arr Time: {end - start}")

# np.append(nl_df["historical_time_stamp"].unique(), nl_df["time_stamp"].unique()).tolist(),
# np.append(ff_df["historical_time_stamp"].unique(), ff_df["time_stamp"].unique()),
# np.append(gm_df["historical_time_stamp"].unique(), gm_df["time_stamp"].unique()),
# np.append(wm_df["historical_time_stamp"].unique(), wm_df["time_stamp"].unique()),

# start = time.time()

# end = time.time()
# print(f"\n\n arr Time: {end - start}")

# start = time.time()
# date_list.sort()
# end = time.time()
# print(f"\n\n List Time: {end - start}")

table_style = {"display": "inline-block", "margin-right": "10px"}


# TODO: Fix table layout to be horizontally aligned correctly
def serve_layout() -> html.Div:
    return html.Div(
        [
            html.Div(html.H2("Websites by Brand"), style={"textAlign": "center"}),
            html.Div(
                className="cb-filters-row",
                children=[
                    html.Div(
                        [
                            html.B("Select Websites"),
                            dcc.Checklist(
                                id="cb-website-checklist",
                                options=[
                                    {"label": website_names["nl"], "value": "nl"},
                                    {"label": website_names["ff"], "value": "ff"},
                                    {"label": website_names["gm"], "value": "gm"},
                                    {"label": website_names["wm"], "value": "wm"},
                                ],
                                value=["nl", "ff", "gm", "wm"],
                                labelStyle={"display": "inline-block"},
                            ),
                            html.Div(id="cb-website-cl-output-container"),
                        ],
                        style={"width": "20%", "textAlign": "center"},
                    ),
                    html.Div(
                        [
                            html.B("Brand"),
                            dcc.Dropdown(
                                id="cb-brand-dropdown",
                                placeholder="Select Brand...",
                            ),
                            html.Div(id="cb-brand-dd-output-container"),
                        ],
                        style={"width": "25%", "textAlign": "center"},
                    ),
                    html.Div(
                        [
                            html.B("Date"),
                            dcc.Dropdown(
                                id="cb-date-dropdown",
                                # options=[{"label": i, "value": i} for i in date_array],
                                # value="latest",
                                # value=date_array[0],
                                clearable=False,
                            ),
                            html.Div(id="cb-date-dd-output-container"),
                        ],
                        style={"width": "25%", "textAlign": "center"},
                    ),
                    html.Div(
                        [
                            html.Button("Download CSV", id="cb-btn-csv"),
                            dcc.Download(id="cb-download-datatable-csv"),
                        ],
                        style={"width": "10%", "vertical-align": "top"},
                    ),
                ],
                style={
                    "display": "flex",
                    "horizontalAlign": "center",
                    "vertical-align": "top",
                },
            ),
            html.Div(
                className="cb-tables-container",
                children=[
                    html.Div(
                        id="cb-nl-table-container",
                        children=[
                            html.Div(
                                html.B(cfg["website_names"]["nl"]),
                                style={"textAlign": "center"},
                            ),
                            dash_table.DataTable(
                                id="cb-nl-table",
                                # columns=[{"name": i, "id": i} for i in nl_df.columns],
                                # data=nl_df.to_dict("records"),
                            ),
                        ],
                        style=table_style,
                    ),
                    html.Div(
                        id="cb-ff-table-container",
                        children=[
                            html.Div(
                                html.B(cfg["website_names"]["ff"]),
                                style={"textAlign": "center"},
                            ),
                            dash_table.DataTable(
                                id="cb-ff-table",
                                # columns=[{"name": i, "id": i} for i in ff_df.columns],
                                # data=ff_df.to_dict("records"),
                            ),
                        ],
                        style=table_style,
                    ),
                    html.Div(
                        id="cb-gm-table-container",
                        children=[
                            html.Div(
                                html.B(cfg["website_names"]["gm"]),
                                style={"textAlign": "center"},
                            ),
                            dash_table.DataTable(
                                id="cb-gm-table",
                                # columns=[{"name": i, "id": i} for i in gm_df.columns],
                                # data=gm_df.to_dict("records"),
                            ),
                        ],
                        style=table_style,
                    ),
                    html.Div(
                        id="cb-wm-table-container",
                        children=[
                            html.Div(
                                html.B(cfg["website_names"]["wm"]),
                                style={"textAlign": "center"},
                            ),
                            dash_table.DataTable(
                                id="cb-wm-table",
                                # columns=[{"name": i, "id": i} for i in wm_df.columns],
                                # data=wm_df.to_dict("records"),
                            ),
                        ],
                        style=table_style,
                    ),
                    # html.Div(
                    #     # html.Div(html.B(cfg["website_names"]["wm"])),
                    #     id="wm-table-container",
                    #     children=[
                    #         html.Div(
                    #             [
                    #                 dash_table.DataTable(
                    #                     id="wm-table",
                    #                     columns=[
                    #                         {"name": i, "id": i} for i in wm_df.columns
                    #                     ],
                    #                     data=wm_df.to_dict("records"),
                    #                 )
                    #             ]
                    #         )
                    #     ],
                    #     style={"display": "inline-block"},
                    # ),
                ],
                style={"display": "inline-block"},
            ),
        ],
    )


@app.callback(
    Output("cb-date-dropdown", "options"),
    Output("cb-date-dropdown", "value"),
    Input("cb-website-checklist", "value"),
)
def update_date_options(selected_websites):
    """Updates date options based on selected websites and selects latest available date as default
    - If multiple websites selected then website list is based on if brand occurs in more than 1 website"""
    filtered_dates, latest = [], None
    total_selected = len(selected_websites)
    if total_selected > 1:
        dates_list = []
        for website in selected_websites:
            dates_list += date_dict[website].keys()
        cnt = Counter(dates_list)
        filtered_dates = [k for k, v in cnt.items() if v > 1]
        latest = filtered_dates[0]
        # print(f"\n\n LEN: {len(filtered_list)}")
    elif total_selected == 1:
        filtered_dates = date_dict[selected_websites[0]].keys()
        latest = next(iter(filtered_dates))

    return [{"label": i, "value": i} for i in filtered_dates], latest


@app.callback(
    Output("cb-brand-dropdown", "options"),
    Input("cb-website-checklist", "value"),
)
def update_brand_options(selected_websites):
    filtered_brands = []
    total_selected = len(selected_websites)
    if total_selected > 1:
        brands_list = []
        for website in selected_websites:
            brands_list += brand_dict[website].keys()
        cnt = Counter(brands_list)
        filtered_brands = [k for k, v in cnt.items() if v > 1]
        # print(f"\n\n LEN: {len(filtered_list)}")
    elif total_selected == 1:
        filtered_brands = brand_dict[selected_websites[0]].keys()
        # print(f"\n\n LEN: {len(filtered_list)}")

    return [{"label": i, "value": i} for i in filtered_brands]

    # start = time.time()
    # arr_list = []
    # first_website = selected_websites[0]
    # for website in selected_websites[1:]:  # Skip first
    #     arr_list.append(brand_dict[website])
    # [np.intersect1d(first_website, A_i) for A_i in arr_list]
    # for idx, website in enumerate(selected_websites):
    #     next_website = selected_websites[idx + 1]
    #     arr_list[idx] = np.intersect1d(brand_dict[website], brand_dict[next_website])

    # for website in selected_websites:
    #     brands_list.append(brand_dict[website].copy())
    # # brands_list.append(*selected_websites.copy())
    # cnt = Counter(brands_list)
    # new_list = [k for k, v in cnt.items() if v > 1]

    # end = time.time()
    # print(f"\n\n List Time: {end - start}")

    # start = time.time()
    # brands_array = np.concatenate(*selected_websites)
    # # creates an array of indices, sorted by unique element
    # idx_sort = np.argsort(brands_array)
    # # sorts records array so all unique elements are together
    # sorted_records_array = brands_array[idx_sort]
    # # returns the unique values, the index of the first occurrence of a value, and the count for each element
    # vals, idx_start, count = np.unique(
    #     sorted_records_array, return_counts=True, return_index=True
    # )
    # # creates an array of indices, sorted by unique element
    # res = np.split(idx_sort, idx_start[1:])
    # # filter them with respect to their size, keeping only items occurring more than once
    # vals = vals[count > 1]
    # res = filter(lambda x: x.size > 1, res)

    # end = time.time()
    # print(f"\n\n Arr Time: {end - start}")


def filter_table_by_brand(df, selected_brand):
    filtered_df = df.loc[df["brand_name"] == selected_brand]
    return filtered_df.drop("brand_name", axis=1, inplace=False)


def filter_table_by_date(website_df, selected_date, date_options):
    dates = [x["value"] for x in date_options]
    # print(f"\n\n Sorted: {dates}")
    # print(f"\n\n Selected: {selected_date}")
    # print(f"\n\n df: {website_df}")
    # formatted_date = date.fromisoformat(selected_date)
    # print(f"DATE: {str(formatted_date)}")
    # print(f"DATE: {dates[0]}")
    if selected_date == dates[0]:
        filtered_df = website_df[
            website_df.columns.difference(
                ["historical_time_stamp", "historical_current_price"]
            )
        ]
        #                          (
        #     [
        #         # "historical_retail_price",
        #         "historical_time_stamp",
        #         # "historical_on_sale",
        #         "historical_current_price",
        #         # "historical_in_stock",
        #     ],
        #     axis=1,
        #     inplace=False,
        # )
        filtered_df = filtered_df.drop_duplicates()
    else:
        filtered_df = website_df[
            website_df.columns.difference(
                ["retail_price", "time_stamp", "on_sale", "current_price", "in_stock"]
            )
        ]
        # filtered_df = website_df.drop(
        #     ["retail_price", "time_stamp", "on_sale", "current_price", "in_stock"],
        #     axis=1,
        #     inplace=False,
        # )
        # print(f"\n\n filtered df: {filtered_df}")
        filtered_df = filtered_df.loc[
            filtered_df["historical_time_stamp"] == date.fromisoformat(selected_date)
        ]
        # print(f"\n\n refiltered df: {filtered_df}")
    return filtered_df


@app.callback(
    Output(component_id="cb-nl-table-container", component_property="style"),
    Output(component_id="cb-ff-table-container", component_property="style"),
    Output(component_id="cb-gm-table-container", component_property="style"),
    Output(component_id="cb-wm-table-container", component_property="style"),
    Input(component_id="cb-website-checklist", component_property="value"),
    Input(component_id="cb-brand-dropdown", component_property="value"),
    Input(component_id="cb-date-dropdown", component_property="value"),
)
def show_hide_tables(selected_websites, selected_brand, selected_date):
    """Dynamically shows or hides website table container based on:
    - whether the website has been selected in website-checklist
    - whether the brand exists on website"""
    hidden = {"display": "none"}
    state_dict = {"nl": hidden, "ff": hidden, "gm": hidden, "wm": hidden}
    # print(f"DATE SELECTED: {selected_date}")
    for website in selected_websites:
        # print(f"Dict for {website}: {date_dict[website]}     ")
        if (
            selected_brand in brand_dict[website]
            and date.fromisoformat(selected_date) in date_dict[website]
        ):
            state_dict[website] = table_style  # Unhide container
    return state_dict["nl"], state_dict["ff"], state_dict["gm"], state_dict["wm"]


@app.callback(
    [Output("cb-nl-table", "data"), Output("cb-nl-table", "columns")],
    [Output("cb-ff-table", "data"), Output("cb-ff-table", "columns")],
    [Output("cb-gm-table", "data"), Output("cb-gm-table", "columns")],
    [Output("cb-wm-table", "data"), Output("cb-wm-table", "columns")],
    Input("cb-website-checklist", "value"),
    Input("cb-date-dropdown", "value"),
    Input("cb-date-dropdown", "options"),
    Input("cb-brand-dropdown", "value"),
)
def update_tables(selected_websites, selected_date, date_options, selected_brand):
    tables_dict = dict.fromkeys(df_dict.keys())
    cols_dict = dict.fromkeys(df_dict.keys())
    websites_to_update = [
        website
        for website in selected_websites
        if date.fromisoformat(selected_date) in date_dict[website]
        and selected_brand in brand_dict[website]
    ]
    # print(f"\n\nUpdating: {websites_to_update}")
    for website in websites_to_update:
        df = df_dict[website]
        # for website, df in df_dict.items():
        filtered_df = filter_table_by_date(df, selected_date, date_options)
        # if selected_brand is not None:
        filtered_df = filter_table_by_brand(filtered_df, selected_brand)
        tables_dict[website] = filtered_df.to_dict("records")
        cols_dict[website] = [{"name": i, "id": i} for i in filtered_df.columns]

    return (
        tables_dict["nl"],
        cols_dict["nl"],
        tables_dict["ff"],
        cols_dict["ff"],
        tables_dict["gm"],
        cols_dict["gm"],
        tables_dict["wm"],
        cols_dict["wm"],
    )

    # for website in selected_websites:
    #     filtered_df = filter_table_by_date(
    #         df_dict[website], selected_date, date_options
    #     )
    #     if selected_brand is not None:
    #         filtered_df = filter_table_by_brand(filtered_df, selected_brand)
    #     table_dict[website] = filtered_df

    # ids = website_df.loc[website_df["code"] == "2597686/1"]
    # print(f"\n\n IDs: {ids['time_stamp']} , {ids['historical_time_stamp']}")

    # filtered_df = filter_table_by_date(website_df, selected_date, date_options)

    # if selected_brand is not None:
    #     filtered_df = filter_table_by_brand(filtered_df, selected_brand)

    # columns = [{"name": i, "id": i} for i in filtered_df.columns]
    # return table_dict["nl"].to_dict("records"), columns


@app.callback(
    Output("cb-download-datatable-csv", "data"),
    Input("cb-btn-csv", "n_clicks"),
    [
        State("cb-nl-table", "data"),
        State("cb-ff-table", "data"),
        State("cb-gm-table", "data"),
        State("cb-wm-table", "data"),
    ],
    # State("website-checklist", "value"),
    State("cb-date-dropdown", "value"),
    State("cb-brand-dropdown", "value"),
    prevent_initial_call=True,
)
def download_table(
    n_clicks, nl_data, ff_data, gm_data, wm_data, selected_date, selected_brand
):
    data_dict = {"nl": nl_data, "ff": ff_data, "gm": gm_data, "wm": wm_data}
    frames_dict = {
        key: pd.DataFrame.from_records(data)
        for key, data in data_dict.items()
        if data is not None
    }
    # Add website name prefix to columns names of each dataframe (in place)
    frames_dict.update(
        (key, df.add_prefix(f"{website_names[key]}_"))
        for key, df in frames_dict.items()
    )
    filename = f"{selected_brand}_{selected_date}_price_comparison.csv"
    merged_df = pd.concat(frames_dict.values(), axis=1, copy=False)
    return dcc.send_data_frame(
        merged_df.to_csv,
        filename=filename,
        index=False,
    )
