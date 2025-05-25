# client/pages/prediction_form.py
from dash import dcc, html, Input, Output, State, register_page, callback, no_update
import dash_bootstrap_components as dbc
import requests
import logging

from client.config.client_settings import client_settings
from client.config.fields_config import get_field_data

register_page(__name__, path='/prediction-form', name="Risk Prediction", title="Prediction Form - PredictHealth")

READABLE_PREDICTION_MAP = {
    "Insufficient_Weight": "Insufficient Weight", "Normal_Weight": "Normal Weight", 
    "Overweight_Level_I": "Overweight Level I", "Overweight_Level_II": "Overweight Level II",
    "Obesity_Type_I": "Obesity Type I", "Obesity_Type_II": "Obesity Type II", "Obesity_Type_III": "Obesity Type III"
}

def layout(): 
    fields = get_field_data()
    print(f"DEBUG (prediction_form.py layout): `fields` recibido: {list(fields.keys() if isinstance(fields, dict) else [])}")
    
    form_elements = []
    if not isinstance(fields, dict) or not fields:
        form_elements.append(html.P("Critical Error: Form field configuration could not be loaded.", style={'color': 'red', 'fontWeight': 'bold'}))
        print("ERROR (prediction_form.py layout): `fields` es inválido o vacío.")
    else:
        for field_id, config_dict in fields.items():
            # ---- DEBUG INTENSO POR CAMPO ----
            print(f"\n--- DEBUG LAYOUT: Procesando campo: '{field_id}' ---")
            print(f"    Configuración recibida para '{field_id}': {config_dict}")
            
            raw_field_type = config_dict.get("type") # Obtiene el valor de la clave "type"
            print(f"    Valor RAW de config_dict.get('type'): '{raw_field_type}' (Tipo: {type(raw_field_type)})")

            processed_field_type = None
            if isinstance(raw_field_type, str):
                processed_field_type = raw_field_type.strip().lower() # Limpia espacios y convierte a minúsculas
                print(f"    Valor PROCESADO de field_type (strip().lower()): '{processed_field_type}'")
            else:
                print(f"    ADVERTENCIA: La clave 'type' NO es un string o está ausente para '{field_id}'.")
            # ---- FIN DEBUG INTENSO ----

            label_component = dbc.Label(config_dict.get('label', f"{field_id}:"), html_for=f'input-pred-{field_id}', className="form-label")
            input_component_for_this_field = None # Renombrado para evitar confusión de scope
            input_id_current = f'input-pred-{field_id}'

            if processed_field_type == "number":
                print(f"    MATCH! '{field_id}' es tipo 'number'. Creando dcc.Input.")
                input_component_for_this_field = dcc.Input(id=input_id_current, type='number', value=config_dict.get("default"), min=config_dict.get("min"), max=config_dict.get("max"), step=config_dict.get("step", 0.1), className="form-control")
            elif processed_field_type == "dropdown":
                print(f"    MATCH! '{field_id}' es tipo 'dropdown'. Creando dcc.Dropdown.")
                options_list = [{'label': opt, 'value': opt} for opt in config_dict.get("options", [])]
                input_component_for_this_field = dcc.Dropdown(id=input_id_current, options=options_list, value=config_dict.get("default"), clearable=False)
            
            if input_component_for_this_field is not None:
                form_elements.append(dbc.Row([dbc.Col(label_component, md=5, className="d-flex align-items-center"), dbc.Col(input_component_for_this_field, md=7)], className="mb-3"))
            else:
                 # Este warning es el que has estado viendo
                 print(f"    WARNING! NO se generó componente para '{field_id}'. "
                       f"Tipo raw: '{raw_field_type}', Tipo procesado: '{processed_field_type}'")
    
    print(f"DEBUG (prediction_form.py layout): Número FINAL de `form_elements` generados: {len(form_elements)}")

    return html.Div(className="page-container-style", children=[
        html.H1("Obesity Risk Prediction Form", className="app-title"),
        html.P("Please complete the following fields to assess your risk.", className="app-subtitle"),
        dbc.Card(dbc.CardBody(form_elements, className="form-card-body-style pt-3"), className="form-card-style"),
        dbc.Row(dbc.Col(dbc.Button('Get Prediction', id='predict-button-prediction', size="lg", className="w-100 mt-4"), width=12),className="mb-3"),
        dcc.Store(id='prediction-data-store'), 
        dcc.Location(id='url-redirector-prediction', refresh=True),
        dbc.Alert(id='prediction-output-prediction', className="mt-3", is_open=False, duration=10000, dismissable=True),
        dbc.Alert(id='error-output-prediction', color="danger", className="mt-3", is_open=False, duration=10000, dismissable=True),
        dcc.Loading(id="loading-output-prediction", type="default", children=html.Div(id="loading-div-prediction"), className="mt-3")
    ])

# --- El Callback no necesita cambios si los IDs del layout son correctos ---
# Pero lo incluyo para que el archivo esté completo
callback_fields_config = get_field_data()
if not isinstance(callback_fields_config, dict) or not callback_fields_config:
    print("CRITICAL ERROR (prediction_form.py callback setup): `callback_fields_config` es inválido o no se cargó. El callback no funcionará como se espera.")
    callback_fields_config = {}

callback_states = [State(f'input-pred-{field_id}', 'value') for field_id in callback_fields_config.keys()]
# Este print es importante para ver qué IDs espera el callback
print(f"DEBUG (prediction_form.py callback setup): IDs de State registrados para callback: {[f'input-pred-{field_id}' for field_id in callback_fields_config.keys()]}")

@callback(
    Output('prediction-data-store', 'data'),
    Output('url-redirector-prediction', 'pathname'),
    Output('error-output-prediction', 'children'),
    Output('error-output-prediction', 'is_open'),
    Output('prediction-output-prediction', 'children'),
    Output('prediction-output-prediction', 'is_open'),
    Output('prediction-output-prediction', 'color'),
    Input('predict-button-prediction', 'n_clicks'),
    callback_states,
    prevent_initial_call=True
)
def handle_prediction_and_store_results_page(n_clicks, *values):
    error_msg = ""
    is_error = False
    success_msg_content = [] 
    is_success = False
    success_color_class = "success-custom" 
    stored_prediction_data = None
    redirect_path = no_update 

    if not callback_fields_config: # Check again inside callback for robustness
        return None, no_update, "Error: Field configuration not loaded for callback.", True, None, False, "light"

    input_data = {}
    field_names_in_order = list(callback_fields_config.keys()) 
    
    if len(values) != len(field_names_in_order):
        error_msg = f"Internal data mismatch. Please contact support."
        is_error = True
        print(f"ERROR (prediction_form.py callback): Mismatch. Values received: {len(values)}, Expected field names: {len(field_names_in_order)}")
        return None, no_update, error_msg, is_error, None, False, "light"

    for i, val in enumerate(values):
        field_name = field_names_in_order[i]
        input_data[field_name] = val
    
    print(f"DEBUG (prediction_form.py callback): Final JSON payload to FastAPI: {input_data}")

    try:
        response = requests.post(client_settings.FASTAPI_PREDICTION_URL, json=input_data)
        response_content = response.json()
        print(f"DEBUG (prediction_form.py callback): FastAPI Response - Status: {response.status_code}, JSON: {response_content}")
        response.raise_for_status()

        stored_prediction_data = response_content 
        redirect_path = "/results"

        pred_label_raw = response_content.get('prediction', '')
        pred_label_display = READABLE_PREDICTION_MAP.get(pred_label_raw, pred_label_raw)
        
        success_msg_content.append(html.H6("Prediction Successful!", className="alert-heading"))
        success_msg_content.append(html.P(f"Result: {pred_label_display}."))
        success_msg_content.append(html.P("You will be redirected to the detailed results page shortly..."))
        is_success = True
        if "Obesity" in pred_label_display or "Overweight" in pred_label_display: success_color_class = "warning-custom"
        elif "Normal" in pred_label_display: success_color_class = "success-custom"
        else: success_color_class = "info-custom"
            
    except requests.exceptions.ConnectionError:
        error_msg = "Connection Error: Could not reach the prediction server. Please ensure it is running."
        is_error = True
    except requests.exceptions.HTTPError as e:
        try: error_detail = e.response.json().get('detail', e.response.text)
        except: error_detail = e.response.text
        error_msg = f"FastAPI Server Error ({e.response.status_code}): {error_detail}"
        is_error = True
    except Exception as e:
        error_msg = f"An unexpected error occurred during prediction: {str(e)}"
        is_error = True
        logging.error(f"Error in prediction_form.py callback (handle_prediction_and_store_results_page): {e}", exc_info=True)
            
    return stored_prediction_data, redirect_path, error_msg, is_error, success_msg_content, is_success, success_color_class