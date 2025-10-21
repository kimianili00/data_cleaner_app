from shiny import render, reactive, ui
from io import BytesIO
import pandas as pd
import numpy as np
from .data_utils import handle_missing_values, transform_columns

def server(input, output, session):
    """Main server logic of the Data Cleaner app."""
    raw_data = reactive.value(pd.DataFrame())
    cleaned_data = reactive.value(pd.DataFrame())
    analysis_data = reactive.value(pd.DataFrame())

    # --- Update selectors dynamically ---
    @reactive.Effect
    def update_selectors():
        df = raw_data()
        if df.empty:
            ui.update_selectize("cols_to_drop", choices=[])
            ui.update_selectize("cols_to_transform", choices=[])
            return
        ui.update_selectize("cols_to_drop", choices=list(df.columns))
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        ui.update_selectize("cols_to_transform", choices=numeric_cols)

    # --- File upload ---
    @reactive.Effect
    @reactive.event(input.file)
    def handle_upload():
        try:
            file = input.file()[0]
            if not file["name"].endswith(".csv"):
                raise ValueError("Only CSV files are supported")

            df = pd.read_csv(file["datapath"])
            raw_data.set(df)
            cleaned_data.set(df.copy())
            analysis_data.set(pd.DataFrame())
            ui.notification_show("File uploaded successfully!", duration=3, type="message")

        except Exception as e:
            ui.notification_show(f"Error loading file: {str(e)}", duration=5, type="error")
            raw_data.set(pd.DataFrame())
            cleaned_data.set(pd.DataFrame())
            analysis_data.set(pd.DataFrame())

    # --- Analyze Data ---
    @reactive.Effect
    @reactive.event(input.analyze)
    def analyze_data():
        if raw_data().empty:
            ui.notification_show("Please upload a file first!", duration=3, type="warning")
            return

        df = raw_data()
        analysis = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str),
            "Missing Values": df.isna().sum(),
            "Unique Values": df.nunique()
        }).sort_values("Missing Values", ascending=False)

        analysis_data.set(analysis)
        ui.notification_show("Analysis completed!", duration=3, type="message")

    # --- Clean Data ---
    @reactive.Effect
    @reactive.event(input.clean)
    def clean_data():
        if raw_data().empty:
            ui.notification_show("No data to clean!", duration=3, type="warning")
            return

        df = cleaned_data().copy()

        # Drop columns
        cols_to_drop = input.cols_to_drop()
        if cols_to_drop:
            df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])

        # Handle NaN
        df = handle_missing_values(df, input.na_action())

        # Transform columns
        df = transform_columns(df, input.cols_to_transform(), input.transform_method())

        cleaned_data.set(df)
        ui.notification_show("Data cleaning applied!", duration=3, type="message")

    # --- Reset ---
    @reactive.Effect
    @reactive.event(input.reset)
    def reset_data():
        if raw_data().empty:
            ui.notification_show("No data to reset!", duration=3, type="warning")
            return
        cleaned_data.set(raw_data().copy())
        analysis_data.set(pd.DataFrame())
        ui.update_selectize("cols_to_drop", selected=[])
        ui.update_radio_buttons("na_action", selected="no_change")
        ui.update_selectize("cols_to_transform", selected=[])
        ui.update_radio_buttons("transform_method", selected="none")
        ui.notification_show("Data reset to original state", duration=3, type="message")

    # --- Download ---
    @render.download(filename="cleaned_data.csv")
    def download():
        df = cleaned_data()
        if df.empty:
            ui.notification_show("No cleaned data to download.", duration=3, type="warning")
            yield b""
        else:
            with BytesIO() as buf:
                df.to_csv(buf, index=False)
                yield buf.getvalue()

    # --- Render main data table ---
    @render.ui
    def data_table_container():
        df = cleaned_data()
        if df.empty:
            return ui.div(
                ui.h4("Data Preview"),
                ui.markdown("Please upload a CSV file to begin."),
                style="min-height: 300px; display:flex;flex-direction:column;justify-content:center;align-items:center;"
            )
        return ui.output_data_frame("data_table")

    @render.data_frame
    def data_table():
        return cleaned_data()

    # --- Render analysis table ---
    @render.ui
    def analysis_table_container():
        df = analysis_data()
        if df.empty:
            return ui.div(
                ui.h4("Data Analysis"),
                ui.markdown("Click 'Analyze' to see data statistics."),
                style="min-height: 300px; display:flex;flex-direction:column;justify-content:center;align-items:center;"
            )
        return ui.output_data_frame("analysis_table")

    @render.data_frame
    def analysis_table():
        return analysis_data()
