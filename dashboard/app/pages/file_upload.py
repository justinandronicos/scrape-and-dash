import base64
import io
from typing import Union
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import pandas as pd
import dash_bootstrap_components as dbc
from file_processor import wm_processor
from models_items.models import WMPriceFileInfo

from app import session, app


def serve_layout() -> html.Div:
    return html.Div(
        [
            dcc.ConfirmDialog(
                id="confirm-upload-dialog",
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Upload Successful!")),
                    dbc.ModalBody([dbc.Label(id="success-modal-body")]),
                ],
                id="upload-success-modal",
                is_open=False,
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("File already uploaded")),
                    dbc.ModalBody(
                        "This file has already been uploaded previously and no updates were found.\n Upload cancelled."
                    ),
                ],
                id="no-update-modal",
                is_open=False,
            ),
            html.Div(html.H2("Upload Product File"), style={"textAlign": "center"}),
            dcc.Upload(
                id="file-upload",
                children=html.Div(["Drag and Drop or ", html.A("Select File")]),
                style={
                    "width": "100%",
                    "height": "60px",
                    "lineHeight": "60px",
                    "borderWidth": "1px",
                    "borderStyle": "dashed",
                    "borderRadius": "5px",
                    "textAlign": "center",
                    "margin": "10px",
                },
            ),
            html.Div(
                id="upload-table-container",
                children=[
                    dash_table.DataTable(
                        id="upload-table"
                        # page_size=50,
                    ),
                ],
            ),
        ]
    )


@app.callback(
    Output("confirm-upload-dialog", "message"),
    Output("confirm-upload-dialog", "displayed"),
    Input("file-upload", "filename"),
)
def display_confirm(filename):
    if filename:
        return (
            f"You have selected '{filename}'\nAre you sure you want to continue?",
            True,
        )
    return None, False


@app.callback(
    Output("file-upload", "contents"),
    Output("file-upload", "filename"),
    Input("confirm-upload-dialog", "cancel_n_clicks"),
)
def cancel_upload(cancel_n_clicks):
    """Set filename and file-upload back to None to enable further attempts"""
    return None, None


@app.callback(
    Output("upload-success-modal", "is_open"),
    Output("success-modal-body", "children"),
    Input("upload-table", "data"),
)
def toggle_success_modal(data):
    num_rows = len(data)
    if num_rows > 1:
        return (
            True,
            f"Successfully uploaded file containing {num_rows} Products",
        )
    return False, None


@app.callback(
    Output("no-update-modal", "is_open"),
    Input("upload-table", "columns"),
    State("file-upload", "filename"),
)
def toggle_no_update_modal(columns, filename):
    if len(columns) == 0 and filename is not None:
        return True
    return False


def check_hash_exists(content_stream: io.BytesIO) -> Union[bytes, None]:
    """Checks if file file has already been uploaded using hash check against WMPriceFileInfo table in database
        and return hash if doesn't already exist

    Args:
        content_stream (io.BytesIO): Binary stream of file contents

    Returns:
        bytes: File hash if hash does not already exist in db else None
    """
    file_hash = wm_processor.get_hash(content_stream)
    existing_hash = session.query(WMPriceFileInfo).filter_by(hash=file_hash).first()
    if existing_hash is None:
        return file_hash
    return None


def parse_contents(contents: str, filename: str) -> Union[pd.DataFrame, None]:
    """Calls check_hash_exists and if hash exists and csv or excel file provided:
        - create pandas dataframe from file contents and pass this to process_file to update database
        - else return None

    Args:
        contents (base64 encoded str): File contents (no matter what file type)
        filename (str): Name of file that was uploaded

    Returns:
        Dataframe | None: Returns none if file hash already exists in database
                        else return pandas dataframe of file contents
    """
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    binary_stream = io.BytesIO(decoded)
    file_hash = check_hash_exists(binary_stream)
    if file_hash is not None and "csv" in filename:
        text_stream = io.StringIO(decoded.decode("utf-8"))
        # Assume that the user uploaded a CSV file
        df = wm_processor.process_file(text_stream, filename, file_hash)
        return df
    elif file_hash is not None and "xls" in filename:
        # Assume that the user uploaded an excel file
        df = wm_processor.process_file(binary_stream, filename)
        return df
    return None


@app.callback(
    Output("upload-table", "data"),
    Output("upload-table", "columns"),
    Input("confirm-upload-dialog", "submit_n_clicks"),
    State("file-upload", "contents"),
    State("file-upload", "filename"),
)
def update_output(submit_n_clicks, contents, filename):
    if contents is None:
        return [{}], []
    if submit_n_clicks:
        # parse_contents returns None if hash_check fails due to file already uploaded previously
        df = parse_contents(contents, filename)
        # set data and columns to empty to trigger no_update_modal if hash_check failed
        return (
            ([{}], [])
            if df is None
            else (df.to_dict("records"), [{"name": i, "id": i} for i in df.columns])
        )

    return [{}], []
