from dash import html, dcc
import dash_bootstrap_components as dbc
from client.config.fields_config import get_fields_config

def generate_input_fields():
    fields = get_fields_config()

    # Dividir los campos en tres grupos lógicos (ajústalo si cambian los campos)
    group1 = ['gender', 'age', 'bmi']
    group2 = ['family_history_with_overweight', 'FAVC', 'FCVC', 'NCP', 'CAEC']
    group3 = ['CH2O', 'SCC', 'FAF', 'TUE', 'CALC']

    def render_fields(field_ids):
        elements = []
        for field_id in field_ids:
            config = fields[field_id]
            label = html.Label(config["label"], className="fw-bold mb-1")

            if config["type"] == "select":
                input_el = dcc.Dropdown(
                    id=field_id,
                    options=[{"label": opt, "value": opt} for opt in config["options"]],
                    placeholder=config["label"],
                    className="mb-2"
                )
            else:
                input_el = dcc.Input(
                    id=field_id,
                    type=config["type"],
                    placeholder=config["label"],
                    debounce=True,
                    className="form-control"
                )
            elements.append(html.Div([label, input_el], className="mb-3"))
        return elements

    return dbc.Container([
        html.H2("Formulario de Evaluación de Obesidad", className="text-center my-4"),

        dbc.Row([
            dbc.Col(html.Div(render_fields(group1)), md=4, xs=12),
            dbc.Col(html.Div(render_fields(group2)), md=4, xs=12),
            dbc.Col(html.Div(render_fields(group3)), md=4, xs=12),
        ], className="gx-4", style={"minHeight": "60vh"}),

        dbc.Row([
            dbc.Col(dbc.Button("Enviar evaluación", id="submit-button", color="warning", className="w-100 mt-2 fw-bold"), width=12),
        ]),

        dbc.Row([
            dbc.Col(html.Div(id="submission-status", className="alert alert-light mt-4 text-center fw-bold"), width=12)
        ]),

        dbc.Row([
            dbc.Col(
                html.Div([
                    html.Div(id="prediction-result", className="alert alert-warning text-center fw-bold", style={"fontSize": "20px"}),
                    dbc.Button("Nuevo estudio", id="reset-form", color="secondary", className="mt-2")
                ],
                id="prediction-bubble",
                className="mt-4 p-3 rounded shadow-sm",
                style={"display": "none", "backgroundColor": "#fff8e1"})
            )
        ])
    ], fluid=True)
