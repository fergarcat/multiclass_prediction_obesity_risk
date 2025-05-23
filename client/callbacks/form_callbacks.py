from dash import Input, Output, State, no_update
from client.config.fields_config import get_field_data
import requests

API_URL = "http://localhost:8000/predict"

def register_callbacks(app):
    fields = get_field_data()
    n_fields = len(fields)

    @app.callback(
        Output("prediction-bubble", "children"),
        Input("predict-btn", "n_clicks"),
        [State(f"input-{i}", "value") for i in range(n_fields)]
    )
    def handle_prediction(n_clicks, *values):
        if not n_clicks:
            return no_update

        field_map = get_field_data()

        input_data = {}
        for i, (field_id, field_config) in enumerate(field_map.items()):
            val = values[i] if i < len(values) else None
            # Conversión básica
            if val in ["yes", "no"]:
                input_data[field_id] = True if val == "yes" else False
            else:
                try:
                    input_data[field_id] = float(val) if val is not None else None
                except:
                    input_data[field_id] = val  # en caso no convertible
        print("Datos enviados a la API:", input_data)

        try:
            response = requests.post(API_URL, json=input_data)
            response.raise_for_status()
            result = response.json()
            return f"🎯 Predicción: {result.get('prediction', '')} — {result.get('header', '')}\n{result.get('text', '')}"
        except Exception as e:
            return f"❌ Error al obtener la predicción: {e}"
