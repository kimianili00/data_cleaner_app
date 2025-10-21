from shiny import ui

# ---------- Custom CSS ----------
custom_css = """
/* ---------- Base Light Theme ---------- */
.card {
    border: 1px solid #dee2e6;
    border-radius: 8px;
    margin-bottom: 16px;
    background-color: #ffffff;
    color: #212529;
}
.card-header {
    background-color: #f8f9fa;
    padding: 10px 16px;
    border-bottom: 1px solid #dee2e6;
    font-weight: bold;
}
.card-body {
    padding: 16px;
}


/* ---------- Buttons ---------- */
.btn-outline-dark {
    border: 1px solid #212529;
    color: #212529;
    background-color: transparent;
    transition: all 0.2s;
}
.btn-outline-dark:hover {
    background-color: #212529;
    color: white;
}

/* ---------- Dark Mode Override ---------- */
html[data-theme='dark'] .card {
    background-color: #1e1e1e;
    border-color: #444;
    color: #f1f1f1;
}
html[data-theme='dark'] .card-header {
    background-color: #2a2a2a;
    border-bottom: 1px solid #444;
}
html[data-theme='dark'] .btn-outline-dark {
    border-color: #f1f1f1;
    color: #f1f1f1;
}
html[data-theme='dark'] .btn-outline-dark:hover {
    background-color: #f1f1f1;
    color: #000;
}

/* ---------- Data Table Background ---------- */
html[data-theme='dark'] table {
    background-color: #222;
    color: #f1f1f1;
}
"""

# ---------- Helper function ----------
def card_block(title, content):
    return ui.div(
        ui.div(title, class_="card-header"),
        ui.div(content, class_="card-body"),
        class_="card"
    )

# ---------- UI Layout ----------
app_ui = ui.page_fluid(
    ui.panel_title("Data Cleaner", window_title="Data Cleaner"),
    ui.tags.style(custom_css),

    ui.navset_pill(
        # Tab 1: Data Cleaning
        ui.nav_panel(
            "Data",
            ui.layout_sidebar(
                ui.sidebar(
                    # Upload CSV
                    card_block(
                        "Upload CSV File",
                        [
                            ui.input_file(
                                id="file", label=None,
                                accept=".csv", multiple=False, width="100%"
                            ),
                            ui.input_action_button(
                                id="analyze", label="Analyze",
                                class_="btn-outline-dark", width="100%"
                            )
                        ]
                    ),

                    # Drop Columns
                    card_block(
                        "Remove Columns",
                        ui.input_selectize(
                            id="cols_to_drop", label=None,
                            choices=[], multiple=True, width="100%"
                        )
                    ),

                    # Missing Values
                    card_block(
                        "Handle Missing Values (NaN)",
                        ui.input_radio_buttons(
                            id="na_action", label=None,
                            choices={
                                "no_change": "No change",
                                "zero": "Replace with 0",
                                "mean": "Replace with column mean",
                                "median": "Replace with column median",
                                "drop": "Drop rows with missing values"
                            },
                            selected="no_change", width="100%"
                        )
                    ),

                    # Transform Columns
                    card_block(
                        "Columns to Transform",
                        ui.input_selectize(
                            id="cols_to_transform", label=None,
                            choices=[], multiple=True, width="100%"
                        )
                    ),

                    # Transformation Type
                    card_block(
                        "Transform Strategy",
                        ui.input_radio_buttons(
                            id="transform_method", label=None,
                            choices={
                                "none": "No transformation",
                                "normalize": "Normalization (0–1)",
                                "standardize": "Standardization (0 mean, 1 variance)"
                            },
                            selected="none", width="100%"
                        )
                    ),

                    # Actions
                    card_block(
                        "Actions",
                        ui.div(
                            [
                                ui.input_action_button(
                                    id="clean", label="Clean",
                                    class_="btn-outline-dark", width="100%"
                                ),
                                ui.input_action_button(
                                    id="reset", label="Reset",
                                    class_="btn-outline-dark", width="100%"
                                ),
                                ui.download_button(
                                    id="download", label="Download",
                                    class_="btn-outline-dark", width="100%"
                                )
                            ],
                            style="gap: 10px; display: flex; flex-direction: column;"
                        )
                    ),

                    ui.input_dark_mode(id="dark_mode", mode="light"),
                    width=300
                ),
                ui.div(ui.output_ui("data_table_container"), style="padding: 15px;")
            )
        ),

        # Tab 2: Analysis
        ui.nav_panel(
            "Analysis",
            ui.div(ui.output_ui("analysis_table_container"), style="padding: 15px;")
        )
    )
)