from dash import dcc, html, Input, Output, State, register_page, callback, no_update, ctx
import dash_bootstrap_components as dbc
import requests
import logging

from client.config.client_settings import client_settings
from client.config.fields_config import get_field_data

register_page(
    __name__, 
    path='/prediction-form', 
    name="Risk Prediction", 
    title="Prediction Form - PredictHealth"
)

READABLE_PREDICTION_MAP = {
    "Insufficient_Weight": "Insufficient Weight", "Normal_Weight": "Normal Weight", 
    "Overweight_Level_I": "Overweight Level I", "Overweight_Level_II": "Overweight Level II",
    "Obesity_Type_I": "Obesity Type I", "Obesity_Type_II": "Obesity Type II", "Obesity_Type_III": "Obesity Type III"
}

def layout(): 
    fields = get_field_data()
    form_elements = []
    if not isinstance(fields, dict) or not fields:
        form_elements.append(html.P("Critical Error: Form field configuration could not be loaded."))
    else:
        for field_id, config_dict in fields.items():
            raw_field_type = config_dict.get("type")
            processed_field_type = None
            if isinstance(raw_field_type, str):
                processed_field_type = raw_field_type.strip().lower()

            label_component = dbc.Label(config_dict.get('label', f"{field_id}:"), html_for=f'input-pred-{field_id}', className="form-label")
            input_component_for_this_field = None
            input_id_current = f'input-pred-{field_id}'

            if processed_field_type == "number":
                input_component_for_this_field = dcc.Input(id=input_id_current, type='number', value=config_dict.get("default"), min=config_dict.get("min"), max=config_dict.get("max"), step=config_dict.get("step", 0.1), className="form-control")
            elif processed_field_type == "dropdown":
                options_list = [{'label': opt, 'value': opt} for opt in config_dict.get("options", [])]
                input_component_for_this_field = dcc.Dropdown(id=input_id_current, options=options_list, value=config_dict.get("default"), clearable=False)
            
            if input_component_for_this_field is not None:
                form_elements.append(dbc.Row([dbc.Col(label_component, md=5, className="d-flex align-items-center"), dbc.Col(input_component_for_this_field, md=7)], className="mb-3"))
            else:
                 print(f"WARNING (prediction_form.py layout)! NO se generó componente para '{field_id}'. Tipo procesado: '{processed_field_type}'")
    
    return html.Div(className="page-container-style", children=[
        html.H1("Obesity Risk Prediction Form", className="app-title"),
        html.P("Please complete the following fields to assess your risk.", className="app-subtitle"),
        dbc.Card(dbc.CardBody(form_elements, className="form-card-body-style pt-3"), className="form-card-style"),
        dbc.Row(dbc.Col(dbc.Button('Get Prediction', id='predict-button-prediction', size="lg", className="w-100 mt-4"), width=12),className="mb-3"),
        # dcc.Store y dcc.Location YA NO ESTÁN AQUÍ, se movieron a app.py o se manejan diferente
        dbc.Alert(id='prediction-output-prediction', className="mt-3", is_open=False, duration=10000, dismissable=True),
        dbc.Alert(id='error-output-prediction', color="danger", className="mt-3", is_open=False, duration=10000, dismissable=True),
        dcc.Loading(id="loading-output-prediction", type="default", children=html.Div(id="loading-div-prediction"), className="mt-3")
    ])

callback_fields_config = get_field_data()
callback_states = [State(f'input-pred-{field_id}', 'value') for field_id in callback_fields_config.keys()]

@callback(
    Output('prediction-data-store', 'data'), # Escribe en el Store global
    Output('app-url', 'pathname'), # Intenta cambiar el pathname del dcc.Location global
    Output('error-output-prediction', 'children'),
    Output('error-output-prediction', 'is_open'),
    Output('prediction-output-prediction', 'children'), # Muestra mensaje de éxito/redirección
    Output('prediction-output-prediction', 'is_open'),
    Output('prediction-output-prediction', 'color'),
    Input('predict-button-prediction', 'n_clicks'),
    callback_states,
    prevent_initial_call=True
)
def handle_prediction_and_store_for_redirect(n_clicks, *values): # Nombre de función más claro
    if not n_clicks: return no_update, no_update, no_update, False, no_update, False, "light"

    print(f"DEBUG (prediction_form.py callback): Botón clickeado. ID del disparador: {ctx.triggered_id}")

    error_msg = ""
    is_error = False
    success_msg_content = [] 
    is_success = False
    success_color_class = "success" 
    stored_prediction_data = no_update # No actualizar store por defecto
    redirect_path = no_update # No redirigir por defecto

    input_data = {}
    field_names_in_order = list(callback_fields_config.keys()) 
    for i, val in enumerate(values): input_data[field_names_in_order[i]] = val
    print(f"DEBUG (prediction_form.py callback): Payload a FastAPI: {input_data}")

    try:
        response = requests.post(client_settings.FASTAPI_PREDICTION_URL, json=input_data)
        response_content = response.json()
        print(f"DEBUG (prediction_form.py callback): FastAPI Response - Status: {response.status_code}, JSON: {response_content}")
        response.raise_for_status()

        stored_prediction_data = response_content # Guarda TODOS los datos de la respuesta
        redirect_path = "/results" # Prepara la redirección

        success_msg_content = html.Div([
            html.H6("Prediction Successful!", className="alert-heading"),
            html.P("Redirecting to results page...")
        ])
        is_success = True
            
    except requests.exceptions.ConnectionError:
        error_msg = "Connection Error: Could not reach server."
        is_error = True
    except requests.exceptions.HTTPError as e:
        try: error_detail = e.response.json().get('detail', e.response.text)
        except: error_detail = e.response.text
        error_msg = f"Server Error ({e.response.status_code}): {error_detail}"
        is_error = True
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        is_error = True
        logging.error(f"Error in prediction_form.py callback: {e}", exc_info=True)
            
    return stored_prediction_data, redirect_path, error_msg, is_error, success_msg_content, is_success, success_color_class