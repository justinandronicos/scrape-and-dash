# # TODO: UNFINISHED

# from datetime import date
# import dash
# import numpy as np
# from dash import dcc
# from dash import html
# from dash.dependencies import Input, Output, State
# import pandas as pd
# from dash import dash_table
# from sqlalchemy.orm import session
# import yaml
# from sqlalchemy import Date
# from collections import Counter

# import time
# import os, sys

# dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(dir))

# # from utilities import get_session
# from models_items.models import (
#     FFBrand,
#     FFCurrentPrice,
#     FFHistoricalPrice,
#     FFProduct,
#     GMBrand,
#     GMCurrentPrice,
#     GMHistoricalPrice,
#     GMProduct,
#     NLBrand,
#     NLCurrentPrice,
#     NLHistoricalPrice,
#     NLProduct,
#     WMBrand,
#     WMCurrentPrice,
#     WMHistoricalPrice,
#     WMProduct,
# )
# from app import session, engine, app

# cfg = yaml.safe_load(open("config.yaml"))

# # engine = create_engine(cfg["db_connection_string"], echo=True)

# website_names = cfg["website_names"]

# # app = dash.Dash(__name__)
# # from dash_app import app

# nl_stmt = (
#     session.query(
#         NLProduct.name,
#         # NLProduct.variant,
#         NLBrand.name.label("brand_name"),
#         # NLCurrentPrice.retail_price,
#         NLCurrentPrice.time_stamp.cast(Date),  # Converted from datetime to date
#         # NLCurrentPrice.on_sale,
#         NLCurrentPrice.current_price,
#         # NLCurrentPrice.in_stock,
#         # NLHistoricalPrice.retail_price.label("historical_retail_price"),
#         NLHistoricalPrice.time_stamp.label("historical_time_stamp").cast(
#             Date
#         ),  # Converted from datetime to date
#         # NLHistoricalPrice.on_sale.label("historical_on_sale"),
#         NLHistoricalPrice.current_price.label("historical_current_price"),
#         # NLHistoricalPrice.in_stock.label("historical_in_stock"),
#         # NLProduct.url,
#     )
#     .join(NLBrand, NLBrand.id == NLProduct.brand_id)
#     .join(NLCurrentPrice, NLCurrentPrice.product_id == NLProduct.id)
#     .join(NLHistoricalPrice, NLHistoricalPrice.product_id == NLProduct.id)
#     .order_by(NLProduct.name)
# ).statement

# nl_df = pd.read_sql(nl_stmt, con=engine)


# ff_stmt = (
#     session.query(
#         FFProduct.name,
#         # FFProduct.variant,
#         FFBrand.name.label("brand_name"),
#         # FFCurrentPrice.retail_price,
#         FFCurrentPrice.time_stamp.cast(Date),  # Converted from datetime to date
#         # FFCurrentPrice.on_sale,
#         FFCurrentPrice.current_price,
#         # FFCurrentPrice.in_stock,
#         # FFHistoricalPrice.retail_price.label("historical_retail_price"),
#         FFHistoricalPrice.time_stamp.label("historical_time_stamp").cast(
#             Date
#         ),  # Converted from datetime to date
#         # FFHistoricalPrice.on_sale.label("historical_on_sale"),
#         FFHistoricalPrice.current_price.label("historical_current_price"),
#         # FFHistoricalPrice.in_stock.label("historical_in_stock"),
#         # FFProduct.url,
#     )
#     .join(FFBrand, FFBrand.id == FFProduct.brand_id)
#     .join(FFCurrentPrice, FFCurrentPrice.product_id == FFProduct.id)
#     .join(FFHistoricalPrice, FFHistoricalPrice.product_id == FFProduct.id)
#     .order_by(FFProduct.name)
# ).statement

# ff_df = pd.read_sql(ff_stmt, con=engine)


# gm_stmt = (
#     session.query(
#         GMProduct.name,
#         # GMProduct.variant,
#         GMBrand.name.label("brand_name"),
#         # GMCurrentPrice.retail_price,
#         GMCurrentPrice.time_stamp.cast(Date),  # Converted from datetime to date
#         # GMCurrentPrice.on_sale,
#         GMCurrentPrice.current_price,
#         # GMCurrentPrice.in_stock,
#         # GMHistoricalPrice.retail_price.label("historical_retail_price"),
#         GMHistoricalPrice.time_stamp.label("historical_time_stamp").cast(
#             Date
#         ),  # Converted from datetime to date
#         # GMHistoricalPrice.on_sale.label("historical_on_sale"),
#         GMHistoricalPrice.current_price.label("historical_current_price"),
#         # GMHistoricalPrice.in_stock.label("historical_in_stock"),
#         # GMProduct.url,
#     )
#     .join(GMBrand, GMBrand.id == GMProduct.brand_id)
#     .join(GMCurrentPrice, GMCurrentPrice.product_id == GMProduct.id)
#     .join(GMHistoricalPrice, GMHistoricalPrice.product_id == GMProduct.id)
#     .order_by(GMProduct.name)
# ).statement

# gm_df = pd.read_sql(gm_stmt, con=engine)


# wm_stmt = (
#     session.query(
#         WMProduct.name,
#         # WMProduct.variant,
#         WMBrand.name.label("brand_name"),
#         # WMCurrentPrice.retail_price,
#         WMCurrentPrice.time_stamp.cast(Date),  # Converted from datetime to date
#         # WMCurrentPrice.on_sale,
#         WMCurrentPrice.current_price,
#         # WMCurrentPrice.in_stock,
#         # WMHistoricalPrice.retail_price.label("historical_retail_price"),
#         WMHistoricalPrice.time_stamp.label("historical_time_stamp").cast(
#             Date
#         ),  # Converted from datetime to date
#         # WMHistoricalPrice.on_sale.label("historical_on_sale"),
#         WMHistoricalPrice.current_price.label("historical_current_price"),
#         # WMHistoricalPrice.in_stock.label("historical_in_stock"),
#         # WMProduct.url,
#     )
#     .join(WMBrand, WMBrand.id == WMProduct.brand_id)
#     .join(WMCurrentPrice, WMCurrentPrice.product_id == WMProduct.id)
#     .join(WMHistoricalPrice, WMHistoricalPrice.product_id == WMProduct.id)
#     .order_by(WMProduct.name)
# ).statement

# wm_df = pd.read_sql(wm_stmt, con=engine)

# df_dict = {
#     "nl": nl_df,
#     "ff": ff_df,
#     "gm": gm_df,
#     "wm": wm_df,
# }

# brand_dict = {
#     "nl": dict.fromkeys(np.sort(nl_df["brand_name"].unique())),
#     "ff": dict.fromkeys(np.sort(ff_df["brand_name"].unique())),
#     "gm": dict.fromkeys(np.sort(gm_df["brand_name"].unique())),
#     "wm": dict.fromkeys(np.sort(wm_df["brand_name"].unique())),
# }

# date_dict = {
#     "nl": dict.fromkeys(
#         sorted(
#             (
#                 np.append(
#                     nl_df["historical_time_stamp"].unique(),
#                     nl_df["time_stamp"].unique(),
#                 )
#             ),
#             reverse=True,
#         )
#     ),
#     "ff": dict.fromkeys(
#         sorted(
#             (
#                 np.append(
#                     ff_df["historical_time_stamp"].unique(),
#                     ff_df["time_stamp"].unique(),
#                 )
#             ),
#             reverse=True,
#         )
#     ),
#     "gm": dict.fromkeys(
#         sorted(
#             (
#                 np.append(
#                     gm_df["historical_time_stamp"].unique(),
#                     gm_df["time_stamp"].unique(),
#                 )
#             ),
#             reverse=True,
#         )
#     ),
#     "wm": dict.fromkeys(
#         sorted(
#             (
#                 np.append(
#                     wm_df["historical_time_stamp"].unique(),
#                     wm_df["time_stamp"].unique(),
#                 )
#             ),
#             reverse=True,
#         )
#     ),
# }

# table_style = {"display": "inline-block", "margin-right": "10px"}

# # TODO: Fix table layout to be horizontally aligned correctly
# app.layout = html.Div(
#     [
#         html.Div(html.H2("Websites by Brand"), style={"textAlign": "center"}),
#         html.Div(
#             className="ps-filters-row",
#             children=[
#                 html.Div(
#                     [
#                         html.B("Product Search"),
#                         dcc.Input(
#                             id="product-search-input",
#                             placeholder="Enter Product Name...",
#                             debounce=True,
#                         ),
#                         # html.Div(id="brand-dd-output-container"),
#                     ],
#                     style={"width": "20%", "textAlign": "center"},
#                 ),
#                 html.Div(
#                     [
#                         html.B("Select Websites"),
#                         dcc.Checklist(
#                             id="ps-website-checklist",
#                             options=[
#                                 {"label": website_names["nl"], "value": "nl"},
#                                 {"label": website_names["ff"], "value": "ff"},
#                                 {"label": website_names["gm"], "value": "gm"},
#                                 {"label": website_names["wm"], "value": "wm"},
#                             ],
#                             value=["nl", "ff", "gm", "wm"],
#                             labelStyle={"display": "inline-block"},
#                         ),
#                         html.Div(id="ps-website-cl-output-container"),
#                     ],
#                     style={"width": "20%", "textAlign": "center"},
#                 ),
#                 html.Div(
#                     [
#                         html.B("Brand"),
#                         dcc.Dropdown(
#                             id="ps-brand-dropdown",
#                             placeholder="Select Brand...",
#                         ),
#                         html.Div(id="ps-brand-dd-output-container"),
#                     ],
#                     style={"width": "20%", "textAlign": "center"},
#                 ),
#                 html.Div(
#                     [
#                         html.B("Date"),
#                         dcc.Dropdown(
#                             id="ps-date-dropdown",
#                             # options=[{"label": i, "value": i} for i in date_array],
#                             # value="latest",
#                             # value=date_array[0],
#                             clearable=False,
#                         ),
#                         html.Div(id="ps-date-dd-output-container"),
#                     ],
#                     style={"width": "25%", "textAlign": "center"},
#                 ),
#                 html.Div(
#                     [
#                         html.Button("Download CSV", id="ps-btn-csv"),
#                         dcc.Download(id="ps-download-datatable-csv"),
#                     ],
#                     style={"width": "10%", "vertical-align": "top"},
#                 ),
#             ],
#             style={
#                 "display": "flex",
#                 "horizontalAlign": "center",
#                 "vertical-align": "top",
#             },
#         ),
#         html.Div(
#             className="ps-tables-container",
#             children=[
#                 html.Div(
#                     id="ps-nl-table-container",
#                     children=[
#                         html.Div(
#                             html.B(cfg["website_names"]["nl"]),
#                             style={"textAlign": "center"},
#                         ),
#                         dash_table.DataTable(
#                             id="ps-nl-table",
#                             # columns=[{"name": i, "id": i} for i in nl_df.columns],
#                             # data=nl_df.to_dict("records"),
#                         ),
#                     ],
#                     style=table_style,
#                 ),
#                 html.Div(
#                     id="ps-ff-table-container",
#                     children=[
#                         html.Div(
#                             html.B(cfg["website_names"]["ff"]),
#                             style={"textAlign": "center"},
#                         ),
#                         dash_table.DataTable(
#                             id="ps-ff-table",
#                             # columns=[{"name": i, "id": i} for i in ff_df.columns],
#                             # data=ff_df.to_dict("records"),
#                         ),
#                     ],
#                     style=table_style,
#                 ),
#                 html.Div(
#                     id="ps-gm-table-container",
#                     children=[
#                         html.Div(
#                             html.B(cfg["website_names"]["gm"]),
#                             style={"textAlign": "center"},
#                         ),
#                         dash_table.DataTable(
#                             id="ps-gm-table",
#                             # columns=[{"name": i, "id": i} for i in gm_df.columns],
#                             # data=gm_df.to_dict("records"),
#                         ),
#                     ],
#                     style=table_style,
#                 ),
#                 html.Div(
#                     id="ps-wm-table-container",
#                     children=[
#                         html.Div(
#                             html.B(cfg["website_names"]["wm"]),
#                             style={"textAlign": "center"},
#                         ),
#                         dash_table.DataTable(
#                             id="ps-wm-table",
#                             # columns=[{"name": i, "id": i} for i in wm_df.columns],
#                             # data=wm_df.to_dict("records"),
#                         ),
#                     ],
#                     style=table_style,
#                 ),
#             ],
#             style={"display": "inline-block"},
#         ),
#     ],
# )


# @app.callback(
#     Output("ps-date-dropdown", "options"),
#     Output("ps-date-dropdown", "value"),
#     Input("ps-website-checklist", "value"),
# )
# def update_date_options(selected_websites):
#     """Updates date options based on selected websites and selects latest available date as default
#     - If multiple websites selected then website list is based on if brand occurs in more than 1 website"""
#     filtered_dates, latest = [], None
#     total_selected = len(selected_websites)
#     if total_selected > 1:
#         dates_list = []
#         for website in selected_websites:
#             dates_list += date_dict[website].keys()
#         cnt = Counter(dates_list)
#         filtered_dates = [k for k, v in cnt.items() if v > 1]
#         latest = filtered_dates[0]
#         # print(f"\n\n LEN: {len(filtered_list)}")
#     elif total_selected == 1:
#         filtered_dates = date_dict[selected_websites[0]].keys()
#         latest = next(iter(filtered_dates))

#     return [{"label": i, "value": i} for i in filtered_dates], latest


# @app.callback(
#     Output("ps-brand-dropdown", "options"),
#     Input("ps-website-checklist", "value"),
# )
# def update_brand_options(selected_websites):
#     filtered_brands = []
#     total_selected = len(selected_websites)
#     if total_selected > 1:
#         brands_list = []
#         for website in selected_websites:
#             brands_list += brand_dict[website].keys()
#         cnt = Counter(brands_list)
#         filtered_brands = [k for k, v in cnt.items() if v > 1]
#         # print(f"\n\n LEN: {len(filtered_list)}")
#     elif total_selected == 1:
#         filtered_brands = brand_dict[selected_websites[0]].keys()
#         # print(f"\n\n LEN: {len(filtered_list)}")

#     return [{"label": i, "value": i} for i in filtered_brands]


# def filter_table_by_brand(df, selected_brand):
#     filtered_df = df.loc[df["brand_name"] == selected_brand]
#     return filtered_df.drop("brand_name", axis=1, inplace=False)


# def filter_table_by_date(website_df, selected_date, date_options):
#     dates = [x["value"] for x in date_options]
#     if selected_date == dates[0]:
#         filtered_df = website_df[
#             website_df.columns.difference(
#                 ["historical_time_stamp", "historical_current_price"]
#             )
#         ]
#         filtered_df = filtered_df.drop_duplicates()
#     else:
#         filtered_df = website_df[
#             website_df.columns.difference(
#                 ["retail_price", "time_stamp", "on_sale", "current_price", "in_stock"]
#             )
#         ]
#         filtered_df = filtered_df.loc[
#             filtered_df["historical_time_stamp"] == date.fromisoformat(selected_date)
#         ]
#     return filtered_df


# @app.callback(
#     Output(component_id="ps-nl-table-container", component_property="style"),
#     Output(component_id="ps-ff-table-container", component_property="style"),
#     Output(component_id="ps-gm-table-container", component_property="style"),
#     Output(component_id="ps-wm-table-container", component_property="style"),
#     Input(component_id="ps-website-checklist", component_property="value"),
#     Input(component_id="ps-brand-dropdown", component_property="value"),
#     Input(component_id="ps-date-dropdown", component_property="value"),
# )
# def show_hide_tables(selected_websites, selected_brand, selected_date):
#     """Dynamically shows or hides website table container based on:
#     - whether the website has been selected in website-checklist
#     - whether the brand exists on website"""
#     hidden = {"display": "none"}
#     state_dict = {"nl": hidden, "ff": hidden, "gm": hidden, "wm": hidden}
#     for website in selected_websites:
#         if (
#             selected_brand in brand_dict[website]
#             and date.fromisoformat(selected_date) in date_dict[website]
#         ):
#             state_dict[website] = table_style  # Unhide container
#     return state_dict["nl"], state_dict["ff"], state_dict["gm"], state_dict["wm"]


# @app.callback(
#     [Output("ps-nl-table", "data"), Output("ps-nl-table", "columns")],
#     [Output("ps-ff-table", "data"), Output("ps-ff-table", "columns")],
#     [Output("ps-gm-table", "data"), Output("ps-gm-table", "columns")],
#     [Output("ps-wm-table", "data"), Output("ps-wm-table", "columns")],
#     Input("ps-website-checklist", "value"),
#     Input("ps-date-dropdown", "value"),
#     Input("ps-date-dropdown", "options"),
#     Input("ps-brand-dropdown", "value"),
# )
# def update_tables(selected_websites, selected_date, date_options, selected_brand):
#     tables_dict = dict.fromkeys(df_dict.keys())
#     cols_dict = dict.fromkeys(df_dict.keys())
#     websites_to_update = [
#         website
#         for website in selected_websites
#         if date.fromisoformat(selected_date) in date_dict[website]
#         and selected_brand in brand_dict[website]
#     ]
#     for website in websites_to_update:
#         df = df_dict[website]
#         filtered_df = filter_table_by_date(df, selected_date, date_options)
#         # if selected_brand is not None:
#         filtered_df = filter_table_by_brand(filtered_df, selected_brand)
#         tables_dict[website] = filtered_df.to_dict("records")
#         cols_dict[website] = [{"name": i, "id": i} for i in filtered_df.columns]

#     return (
#         tables_dict["nl"],
#         cols_dict["nl"],
#         tables_dict["ff"],
#         cols_dict["ff"],
#         tables_dict["gm"],
#         cols_dict["gm"],
#         tables_dict["wm"],
#         cols_dict["wm"],
#     )


# @app.callback(
#     Output("ps-download-datatable-csv", "data"),
#     Input("ps-btn-csv", "n_clicks"),
#     [
#         State("ps-nl-table", "data"),
#         State("ps-ff-table", "data"),
#         State("ps-gm-table", "data"),
#         State("ps-wm-table", "data"),
#     ],
#     # State("website-checklist", "value"),
#     State("ps-date-dropdown", "value"),
#     State("ps-brand-dropdown", "value"),
#     prevent_initial_call=True,
# )
# def download_table(
#     n_clicks, nl_data, ff_data, gm_data, wm_data, selected_date, selected_brand
# ):
#     data_dict = {"nl": nl_data, "ff": ff_data, "gm": gm_data, "wm": wm_data}
#     frames_dict = {
#         key: pd.DataFrame.from_records(data)
#         for key, data in data_dict.items()
#         if data is not None
#     }
#     # Add website name prefix to columns names of each dataframe (in place)
#     frames_dict.update(
#         (key, df.add_prefix(f"{website_names[key]}_"))
#         for key, df in frames_dict.items()
#     )
#     filename = f"{selected_brand}_{selected_date}_price_comparison.csv"
#     merged_df = pd.concat(frames_dict.values(), axis=1, copy=False)
#     return dcc.send_data_frame(
#         merged_df.to_csv,
#         filename=filename,
#         index=False,
#     )


# if __name__ == "__main__":
#     app.run_server(debug=True)
