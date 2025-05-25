# client/pages/results.py
from dash import dcc, html, Input, Output, State, callback, register_page, no_update, ctx
import dash_bootstrap_components as dbc
import logging
import json

register_page(
    __name__, 
    path='/results', 
    name="Results", 
    title="Your Evaluation Results - PredictHealth"
)

def layout(**kwargs): 
    print(f"DEBUG (results.py layout): Layout para /results renderizado. kwargs: {kwargs}")
    return html.Div(className="page-container-style", children=[
        html.H1("Your Evaluation Results", className="app-title mb-4"),
        html.Div(id="results-dynamic-content", children=[
            # Este es el contenido inicial ANTES de que el callback se ejecute por primera vez
            html.P("Awaiting prediction data...", id="results-initial-placeholder") 
        ]),
        dbc.Row(
            dbc.Col(
                dcc.Link(
                    dbc.Button("Perform New Assessment", size="lg", className="w-100 mt-4"),
                    href="/prediction-form"
                ),
            width={"size": 6, "offset": 3}
            ), className="mt-5"
        )
    ])

@callback(
    Output('results-dynamic-content', 'children'),
    Input('app-url', 'pathname'),         # <--- DISPARADOR PRINCIPAL POR CAMBIO DE URL
    State('prediction-data-store', 'data'), # <--- LEEMOS EL ESTADO DEL STORE, NO ES UN INPUT DIRECTO
    # prevent_initial_call=True # Cambiado a True, para que no se ejecute al inicio de la app
                               # solo cuando 'app-url' (pathname) cambie A /results
                               # OJO: Si el usuario navega DIRECTO a /results (ej. refresh),
                               # este callback se disparará porque el pathname es /results.
)
def update_results_on_navigation(current_pathname, stored_data):
    print(f"DEBUG (results.py callback 'update_results_on_navigation'): Disparado.")
    print(f"    Current Pathname: {current_pathname}")

    # Solo renderizamos el contenido si estamos EFECTIVAMENTE en la página /results
    if current_pathname == '/results':
        print(f"    Estamos en /results.")
        if stored_data:
            print(f"    Datos del Store encontrados: {json.dumps(stored_data, indent=2)}")
            
            prediction_raw = stored_data.get('prediction', 'N/A')
            bmi_value_from_store = stored_data.get('bmi', 'N/A') # Lo que el backend calculó
            tip_text = stored_data.get('tip_text', 'No specific tip available.')
            # Podrías añadir confidence, input_data, tip_header si los necesitas aquí.
            
            # Muestra tu layout simplificado y luego el completo.
            return html.Div([
                html.H3("¡Hola Mundo desde Results! La Redirección y el Store Funcionaron."),
                html.Hr(),
                dbc.Alert(f"Predicción Recibida: {prediction_raw}", color="info", className="mt-2"),
                dbc.Alert(f"BMI Calculado por Backend: {bmi_value_from_store}", color="info", className="mt-2"),
                dbc.Alert(f"Consejo del Backend: {tip_text}", color="success", className="mt-2"),
                html.H5("Datos completos del Store para depuración:", className="mt-4"),
                html.Pre(json.dumps(stored_data, indent=2), style={'maxHeight': '300px', 'overflowY': 'auto'})
            ])
        else:
            print(f"    No hay datos en el store al llegar a /results. Mostrando 'sin datos'.")
            return dbc.Alert("No prediction data currently available in store. Please perform an assessment.", color="warning")
    
    # Si no estamos en /results, este callback no debería cambiar el contenido de ESTA página.
    # `page_container` maneja el cambio a otras páginas.
    # Devolver no_update asegura que si este callback se dispara por alguna razón
    # cuando no estamos en /results, no interfiera con el layout de otra página.
    return no_update