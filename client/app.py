import dash
from dash import html
import dash_bootstrap_components as dbc
from client.components.input_form import generate_input_fields
from client.callbacks.form_callbacks import register_callbacks

GRAY_BG = "#F8F9FA"
PERSIMON = "#FFB347"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "Predicción de Riesgo de Obesidad"
server = app.server

app.layout = html.Div(
    style={'backgroundColor': GRAY_BG, 'padding': '10px', 'minHeight': '100vh'},
    children=[
        dbc.NavbarSimple(
            brand="Predicción de Obesidad",
            brand_href="#",
            color="warning",
            dark=False,
            className="mb-4 shadow-sm"
        ),
        generate_input_fields(),
        html.Footer(
            html.Div("© 2025 Proyecto ML - Universidad", className="text-center text-muted mt-4 pb-2"),
            className="bg-light mt-5 pt-3"
        ),
    ]
)

register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8050)
