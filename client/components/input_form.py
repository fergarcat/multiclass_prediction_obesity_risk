from dash import html, dcc
import dash_bootstrap_components as dbc
from client.config.fields_config import get_field_data

def generate_input_fields():
    fields = get_field_data()

    input_elements = []

    for i, (field_id, field_config) in enumerate(fields.items()):
        label_text = field_config["label"]
        description_text = field_config.get("description", "")  # description opcional
        label = html.Label(label_text, className="fw-bold mb-1")

        if field_config["type"] == "select":
            input_el = dcc.Dropdown(
                id=f"input-{i}",
                options=[{"label": opt, "value": opt} for opt in field_config["options"]],
                placeholder=f"Seleccione {label_text}",
                className="mb-1"
            )
        else:
            input_el = dcc.Input(
                id=f"input-{i}",
                type="number",
                placeholder=f"Ingrese {label_text}",
                debounce=True,
                className="form-control"
            )

        description_el = html.Small(description_text, className="text-muted")

        input_elements.append(html.Div([label, input_el, description_el], className="mb-3"))

    # Dividir en columnas (igual que antes)
    col_count = len(input_elements)
    third = col_count // 3 + (1 if col_count % 3 else 0)
    layout = dbc.Row([
        dbc.Col(input_elements[:third], md=4, xs=12),
        dbc.Col(input_elements[third:2*third], md=4, xs=12),
        dbc.Col(input_elements[2*third:], md=4, xs=12),
    ], className="gx-4", style={"minHeight": "60vh"})

    return dbc.Container([
        html.H2("Formulario de Evaluación de Obesidad", className="text-center my-4"),
        layout,
        dbc.Row([
            dbc.Col(
                dbc.Button("Predecir", id="predict-btn", color="primary", className="w-100 mt-2 fw-bold"),
                width=12
            )
        ]),
        dbc.Row([
            dbc.Col(html.Div(id="prediction-bubble", className="mt-4"), width=12)
        ])
    ], fluid=True)
