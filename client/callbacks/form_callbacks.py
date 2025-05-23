import requests
from dash import Input, Output, State
from client.services.queries import insert_user_input
from client.config.fields_config import get_fields_config
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

APR_COLOR = "#FFB347"

def register_callbacks(app):
    fields = get_fields_config()
    field_ids = list(fields.keys())

    # Callback: Enviar formulario y mostrar predicción
    @app.callback(
        Output("submission-status", "children"),
        Output("prediction-result", "children"),
        Output("prediction-bubble", "style"),
        Input("submit-button", "n_clicks"),
        [State(field_id, "value") for field_id in field_ids]
    )
    def handle_submit(n_clicks, *values):
        if n_clicks is None or n_clicks == 0:
            raise PreventUpdate

        data = {k: v for k, v in zip(field_ids, values)}

        # Guardar en base de datos
        try:
            insert_user_input(data)
        except Exception as e:
            return dbc.Alert(f"❌ Error al guardar: {e}", color="danger"), "", {"display": "none"}

        # Llamar al endpoint de predicción
        try:
            response = requests.post("http://127.0.0.1:8000/predict", json=data)
            response.raise_for_status()
            prediction = response.json().get("prediction", "Sin resultado")
        except Exception as e:
            return "✅ Datos guardados. ❌ Error en predicción: " + str(e), "", {"display": "none"}

        # Mostrar resultado en la burbuja
        return (
            dbc.Alert("✅ Datos enviados correctamente.", color="success", className="text-center"),
            f"Resultado del análisis: {prediction}",
            {"display": "block"}
        )

    # Callback: Resetear formulario
    @app.callback(
        [Output(field_id, "value") for field_id in field_ids] +
        [
            Output("submission-status", "children"),
            Output("prediction-result", "children"),
            Output("prediction-bubble", "style")
        ],
        Input("reset-form", "n_clicks"),
        prevent_initial_call=True
    )
    def reset_form(n_clicks):
        if not n_clicks:
            raise PreventUpdate

        empty_fields = [None for _ in field_ids]
        return (
            *empty_fields,
            "", "", {"display": "none"}
        )
