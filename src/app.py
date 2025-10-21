from shiny import App
from .ui_layout import app_ui
from .server_logic import server

# Entry point for running the app
app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
