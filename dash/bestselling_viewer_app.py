import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import yaml
from sqlalchemy import Date
from datetime import date

# import os
# import sys

# dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(dir))

# from dash_app import session, engine, app

# from utilities import get_session
from models import (
    FFBestSelling,
    FFBrand,
    FFProduct,
    NLBestSelling,
    NLBrand,
    NLProduct,
)
from app import app, session, engine

cfg = yaml.safe_load(open("config.yaml"))
# engine = create_engine(cfg["db_connection_string"], echo=True)

website_names = cfg["website_names"]

# app = dash.Dash(__name__)
# from dash_app import app

nl_stmt = (
    session.query(
        NLBestSelling.ranking,
        NLProduct.name,
        NLBrand.name.label("brand_name"),
        NLProduct.url,
        NLBestSelling.category,
        NLBestSelling.time_stamp.cast(Date),
    )
    .join(NLProduct, NLProduct.id == NLBestSelling.product_id)
    .join(NLBrand, NLBrand.id == NLProduct.brand_id)
    .order_by(NLBestSelling.ranking)
).statement

nl_df = pd.read_sql(nl_stmt, con=engine)

ff_stmt = (
    session.query(
        FFBestSelling.ranking,
        FFProduct.name,
        FFBrand.name.label("brand_name"),
        FFProduct.url,
        FFBestSelling.category,
        FFBestSelling.time_stamp.cast(Date),
    )
    .join(FFProduct, FFProduct.id == FFBestSelling.product_id)
    .join(FFBrand, FFBrand.id == FFProduct.brand_id)
    .order_by(FFBestSelling.ranking)
).statement

ff_df = pd.read_sql(ff_stmt, con=engine)

# dates_dict = {
#     "nl": nl_df["time_stamp"].unique(),
#     "ff": ff_df["time_stamp"].unique(),
# }

layout = html.Div(
    [
        html.Div(html.H2("Best Selling Products"), style={"textAlign": "center"}),
        html.Div(
            className="bs-filters-row",
            children=[
                html.Div(
                    [
                        html.B("Website"),
                        dcc.Dropdown(
                            id="bs-website-dropdown",
                            options=[
                                {"label": website_names["nl"], "value": "nl"},
                                {"label": website_names["ff"], "value": "ff"},
                            ],
                            value="nl",
                            clearable=False,
                        ),
                        # html.Div(id="website-dd-output-container"),
                    ],
                    style={"width": "25%", "textAlign": "center"},
                ),
                html.Div(
                    [
                        html.B("Date"),
                        dcc.Dropdown(
                            id="bs-date-dropdown",
                            value="latest",
                            clearable=False,
                        ),
                        # html.Div(id="date-dd-output-container"),
                    ],
                    style={"width": "25%", "textAlign": "center"},
                ),
                html.Div(
                    [
                        html.B("Category"),
                        dcc.Dropdown(
                            id="bs-category-dropdown",
                        ),
                        # html.Div(id="date-dd-output-container"),
                    ],
                    style={"width": "25%", "textAlign": "center"},
                ),
                html.Div(
                    [
                        html.Button("Download CSV", id="bs-btn-csv"),
                        dcc.Download(id="bs-download-datatable-csv"),
                    ],
                    style={"width": "10%"},
                ),
            ],
            style={"display": "flex", "horizontalAlign": "center"},
        ),
        html.Div(
            [
                dash_table.DataTable(
                    id="bs-table",
                    columns=[{"name": i, "id": i} for i in nl_df.columns],
                    data=nl_df.to_dict("records"),
                    page_size=50,
                )
            ]
        ),
    ]
)


@app.callback(
    Output("bs-category-dropdown", "options"),
    Output("bs-category-dropdown", "value"),
    Input("bs-website-dropdown", "value"),
)
def update_category_options(selected_website):
    """Updates category options based on selected website and defaults to no selection"""
    category_df = (
        nl_df["category"]
        if selected_website == "nl"
        else ff_df["category"]
        if selected_website == "ff"
        else None
    )
    sorted_df = sorted(category_df.unique())
    return [{"label": i, "value": i} for i in sorted_df], None


@app.callback(
    Output("bs-date-dropdown", "options"),
    Output("bs-date-dropdown", "value"),
    Input("bs-website-dropdown", "value"),
    Input("bs-category-dropdown", "value"),
    State("bs-date-dropdown", "value"),
)
def update_date_options_value(selected_website, selected_category, selected_date):
    """Updates date options after website selected
    - If triggered by website dropdown: sets selected date to latest available
    - If triggered by category dropdown: keeps currently selected date"""
    if selected_category:
        filtered_df = (
            nl_df.loc[nl_df["category"] == selected_category]
            if selected_website == "nl"
            else ff_df.loc[ff_df["category"] == selected_category]
            if selected_website == "ff"
            else None
        )
        date_array = filtered_df["time_stamp"].unique()

    else:
        date_array = (
            nl_df["time_stamp"].unique()
            if selected_website == "nl"
            else ff_df["time_stamp"].unique()
            if selected_website == "ff"
            else None
        )
        # date_array = dates_dict[selected_website]
    date_array[::-1].sort()  # Sort dates descending

    # Check if callback triggered by website or category change
    ctx = dash.callback_context
    trigger = ctx.triggered[0]["prop_id"].split(".")[0]

    # print(f"\n This is the trigger: {trigger}")

    if trigger == "bs-category-dropdown" and selected_category is not None:
        return [{"label": i, "value": i} for i in date_array], selected_date
    else:
        return [{"label": i, "value": i} for i in date_array], date_array[0]


@app.callback(
    Output("bs-table", "data"),
    Output("bs-table", "columns"),
    Input("bs-website-dropdown", "value"),
    Input("bs-date-dropdown", "value"),
    Input("bs-date-dropdown", "options"),
    Input("bs-category-dropdown", "value"),
)
def update_table(selected_website, selected_date, date_options, selected_category):
    website_df = (
        nl_df
        if selected_website == "nl"
        else ff_df
        if selected_website == "ff"
        else None
    )
    dates = [x["value"] for x in date_options]
    filtered_df = website_df.loc[
        website_df["time_stamp"] == date.fromisoformat(selected_date)
    ]
    if selected_category:
        filtered_df = filtered_df.loc[filtered_df["category"] == selected_category]
    # print(f"\n\n LEN: {len(filtered_df)}")
    # filtered_df = filtered_df.drop(["time_stamp"], axis=1, inplace=False)
    # else:
    #     filtered_df = filtered_df.drop(
    #         ["category", "time_stamp"], axis=1, inplace=False
    #     )
    filtered_df = filtered_df.drop_duplicates(subset=["ranking", "name"])
    columns = [{"name": i, "id": i} for i in filtered_df.columns]
    # print(f"\n\n {filtered_df.iloc[0, 1] == filtered_df.iloc[1, 1]}")
    return filtered_df.to_dict("records"), columns


@app.callback(
    Output("bs-download-datatable-csv", "data"),
    Input("bs-btn-csv", "n_clicks"),
    State("bs-table", "data"),
    State("bs-website-dropdown", "value"),
    State("bs-date-dropdown", "value"),
    State("bs-category-dropdown", "value"),
    prevent_initial_call=True,
)
def download_table(n_clicks, data, selected_website, selected_date, selected_category):
    df = pd.DataFrame.from_records(data)
    if selected_category:
        filename = f"{website_names[selected_website]}_{selected_category}_best_selling_list_{selected_date}.csv"
    else:
        filename = (
            f"{website_names[selected_website]}_best_selling_list_{selected_date}.csv"
        )
    return dcc.send_data_frame(
        df.to_csv,
        filename=filename,
        index=False,
    )


# if __name__ == "__main__":
#     app.run_server(debug=True)
