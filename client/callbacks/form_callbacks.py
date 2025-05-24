# client/callbacks/form_callbacks.py
from dash import Output, Input, State, no_update
import requests
from client.config.client_settings import client_settings
from client.config.fields_config import get_field_data
import logging # Para logging adicional en el cliente si es necesario

# Configura un logger para el cliente de Dash si quieres ver mensajes de logging estructurados
# (aparte de los prints que ya tienes). Esto es opcional, los prints ya te darán feedback inmediato.
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - DashClient - %(levelname)s - %(message)s')


def register_callbacks(app):
    fields_config = get_field_data()
    if not fields_config:
        logging.error("ERROR (client): fields_config is empty. Cannot register dynamic states. Check fields_config.py.")
        return 

    input_states = [State(f'input-{field_id}', 'value') for field_id in fields_config.keys()]
    print(f"DEBUG (client): States registered from fields_config.keys(): {list(fields_config.keys())}") 

    @app.callback(
        [Output('prediction-output', 'children'),
         Output('prediction-output', 'is_open'),
         Output('prediction-output', 'color'),
         Output('error-output', 'children'),
         Output('error-output', 'is_open'),
         Output('loading-div', 'children')],
        [Input('predict-button', 'n_clicks')],
        input_states
    )
    def handle_prediction(n_clicks, *values):
        if not n_clicks:
            return no_update, no_update, no_update, no_update, no_update, no_update

        prediction_output_text = ""
        prediction_alert_open = False
        prediction_alert_color = ""
        error_output_text = ""
        error_alert_open = False
        
        input_data = {}
        field_names_in_order = list(fields_config.keys())
        
        if len(values) != len(field_names_in_order):
            error_output_text = f"Error interno: Número de inputs esperados no coincide con los recibidos. Recibidos: {len(values)}, Esperados: {len(field_names_in_order)}."
            error_alert_open = True
            logging.error(error_output_text + f" Detalle: Valores recibidos: {values}")
            return prediction_output_text, prediction_alert_open, prediction_alert_color, error_output_text, error_alert_open, ""

        # =======================================================
        # DEBUG: Recolecta los datos de los inputs y mapea
        print("--- DEBUG CLIENT SIDE DATA ---")
        for i, val in enumerate(values):
            field_name = field_names_in_order[i]
            input_data[field_name] = val
            print(f"DEBUG (client): Collected input -> {field_name}: '{val}' (Type: {type(val).__name__})")
        print(f"DEBUG (client): Final JSON payload to FastAPI: {input_data}")
        print(f"DEBUG (client): Calling FastAPI at: {client_settings.FASTAPI_PREDICTION_URL}")
        # =======================================================

        try:
            response = requests.post(client_settings.FASTAPI_PREDICTION_URL, json=input_data)
            print(f"DEBUG (client): FastAPI Response Status: {response.status_code}")
            # Intenta imprimir la respuesta JSON o texto incluso si hay un error
            try:
                response_content = response.json()
                print(f"DEBUG (client): FastAPI Response JSON: {response_content}")
            except requests.exceptions.JSONDecodeError:
                response_content = response.text
                print(f"DEBUG (client): FastAPI Response Text: {response_content}")


            response.raise_for_status() # Lanza HTTPError si status no es 2xx

            # Si llegamos aquí, la respuesta fue 2xx
            result = response_content # Ya tenemos el contenido parseado
            
            prediction_label = result.get('prediction', 'No disponible')
            confidence = result.get('confidence')
            bmi_value = result.get('bmi')

            readable_label_map = {
                "Insufficient_Weight": "Bajo Peso",
                "Normal_Weight": "Peso Normal",
                "Overweight_Level_I": "Sobrepeso Nivel I",
                "Overweight_Level_II": "Sobrepeso Nivel II",
                "Obesity_Type_I": "Obesidad Tipo I",
                "Obesity_Type_II": "Obesidad Tipo II",
                "Obesity_Type_III": "Obesidad Tipo III"
            }
            
            display_label = readable_label_map.get(prediction_label, prediction_label)

            prediction_output_text = f"La predicción de riesgo de obesidad es: **{display_label}**."
            if confidence is not None:
                prediction_output_text += f" (Confianza: {confidence:.2f})."
            if bmi_value is not None:
                prediction_output_text += f" Tu BMI calculado es: **{bmi_value:.2f}**."

            prediction_alert_open = True
            prediction_alert_color = "success"

        except requests.exceptions.ConnectionError:
            error_output_text = "Error de conexión: Asegúrate que el servidor FastAPI está corriendo en " + client_settings.FASTAPI_PREDICTION_URL
            error_alert_open = True
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            error_detail = e.response.json().get('detail', e.response.text) if e.response.text else "N/A"
            error_output_text = f"Error del servidor FastAPI ({status_code}): {error_detail}"
            error_alert_open = True
            logging.error(f"HTTP Error: {status_code}, Detail: {error_detail}", exc_info=True)
        except Exception as e:
            error_output_text = f"Ocurrió un error inesperado: {e}"
            error_alert_open = True
            logging.error(f"Unexpected error: {e}", exc_info=True)
        
        return (
            prediction_output_text,
            prediction_alert_open,
            prediction_alert_color,
            error_output_text,
            error_alert_open,
            ""
        )