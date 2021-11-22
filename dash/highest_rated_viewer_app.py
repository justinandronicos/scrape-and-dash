from datetime import date
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
from dash import dash_table
from sqlalchemy.orm import session
import yaml
from sqlalchemy import create_engine, Date

# dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(dir))

# from utilities import get_session
from models import (
    FFHighestRated,
    FFBrand,
    FFProduct,
    NLHighestRated,
    NLBrand,
    NLProduct,
)
from dash_app import session, engine, app

cfg = yaml.safe_load(open("config.yaml"))

# engine = create_engine(cfg["db_connection_string"], echo=True)

website_names = cfg["website_names"]

# app = dash.Dash(__name__)
# from dash_app import app

nl_stmt = (
    session.query(
        NLHighestRated.ranking,
        NLProduct.name,
        NLHighestRated.rating.label("rating (5-star)"),
        NLHighestRated.review_count,
        NLBrand.name.label("brand_name"),
        NLProduct.url,
        NLHighestRated.category,
        NLHighestRated.time_stamp.cast(Date),
    )
    .join(NLProduct, NLProduct.id == NLHighestRated.product_id)
    .join(NLBrand, NLBrand.id == NLProduct.brand_id)
    .order_by(NLHighestRated.ranking)
).statement

nl_df = pd.read_sql(nl_stmt, con=engine)

ff_stmt = (
    session.query(
        FFHighestRated.ranking,
        FFProduct.name,
        FFHighestRated.rating.label("rating (5-star)"),
        FFHighestRated.review_count,
        FFBrand.name.label("brand_name"),
        FFProduct.url,
        FFHighestRated.category,
        FFHighestRated.time_stamp.cast(Date),
    )
    .join(FFProduct, FFProduct.id == FFHighestRated.product_id)
    .join(FFBrand, FFBrand.id == FFProduct.brand_id)
    .order_by(FFHighestRated.ranking)
).statement

ff_df = pd.read_sql(ff_stmt, con=engine)

layout = html.Div(
    [
        html.Div(html.H2("Highest Rated Products"), style={"textAlign": "center"}),
        html.Div(
            className="hr-filters_row",
            children=[
                html.Div(
                    [
                        html.B("Website"),
                        dcc.Dropdown(
                            id="hr-website-dropdown",
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
                            id="hr-date-dropdown",
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
                            id="hr-category-dropdown",
                        ),
                        # html.Div(id="date-dd-output-container"),
                    ],
                    style={"width": "25%", "textAlign": "center"},
                ),
                html.Div(
                    [
                        html.Button("Download CSV", id="hr-btn-csv"),
                        dcc.Download(id="hr-download-datatable-csv"),
                    ],
                    style={"width": "10%"},
                ),
            ],
            style={"display": "flex", "horizontalAlign": "center"},
        ),
        html.Div(
            [
                dash_table.DataTable(
                    id="hr-table",
                    columns=[{"name": i, "id": i} for i in nl_df.columns],
                    data=nl_df.to_dict("records"),
                    page_size=50,
                )
            ]
        ),
    ]
)


@app.callback(
    Output("hr-category-dropdown", "options"),
    Output("hr-category-dropdown", "value"),
    Input("hr-website-dropdown", "value"),
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
    Output("hr-date-dropdown", "options"),
    Output("hr-date-dropdown", "value"),
    Input("hr-website-dropdown", "value"),
    Input("hr-category-dropdown", "value"),
)
def update_date_options_value(selected_website, selected_category):
    """Updates date options after website selected and sets selected date to latest available by default"""
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
    date_array[::-1].sort()  # Sort dates descending
    return [{"label": i, "value": i} for i in date_array], date_array[0]


@app.callback(
    Output("hr-table", "data"),
    Output("hr-table", "columns"),
    Input("hr-website-dropdown", "value"),
    Input("hr-date-dropdown", "value"),
    Input("hr-date-dropdown", "options"),
    Input("hr-category-dropdown", "value"),
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
    filtered_df = filtered_df.drop_duplicates(subset=["ranking", "name"])
    columns = [{"name": i, "id": i} for i in filtered_df.columns]
    return filtered_df.to_dict("records"), columns


@app.callback(
    Output("hr-download-datatable-csv", "data"),
    Input("hr-btn-csv", "n_clicks"),
    State("hr-table", "data"),
    State("hr-website-dropdown", "value"),
    State("hr-date-dropdown", "value"),
    State("hr-category-dropdown", "value"),
    prevent_initial_call=True,
)
def download_table(n_clicks, data, selected_website, selected_date, selected_category):
    df = pd.DataFrame.from_records(data)
    if selected_category:
        filename = f"{website_names [selected_website]}_{selected_category}_highest_rated_list_{selected_date}.csv"
    else:
        filename = (
            f"{website_names [selected_website]}_highest_rated_list_{selected_date}.csv"
        )
    return dcc.send_data_frame(
        df.to_csv,
        filename=filename,
        index=False,
    )


# if __name__ == "__main__":
#     app.run_server(debug=True)
