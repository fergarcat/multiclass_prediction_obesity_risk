# client/pages/results.py
from dash import dcc, html, Input, Output, State, register_page, callback, no_update
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import logging

# El decorador register_page para que Dash conozca esta página
register_page(__name__, path='/results', name="Results", title="Your Evaluation Results - PredictHealth")

# --- Constantes de Configuración y Mapeo ---
READABLE_PREDICTION_MAP = {
    "Insufficient_Weight": "Insufficient Weight", "Normal_Weight": "Normal Weight", 
    "Overweight_Level_I": "Overweight Level I", "Overweight_Level_II": "Overweight Level II",
    "Obesity_Type_I": "Obesity Type I", "Obesity_Type_II": "Obesity Type II", "Obesity_Type_III": "Obesity Type III"
}
BMI_RANGES = {
    "Underweight (Severe)": (0, 15.99), "Underweight (Moderate)": (16, 16.99), "Underweight (Mild)": (17, 18.49),
    "Normal Weight": (18.5, 24.99), "Overweight": (25, 29.99),
    "Obesity Class I": (30, 34.99), "Obesity Class II": (35, 39.99), "Obesity Class III (Morbid)": (40, 60) 
}
BMI_COLORS = { 
    "Underweight (Severe)": "#FBD0AD", "Underweight (Moderate)": "#F9AF78", "Underweight (Mild)": "#F58342",   
    "Normal Weight": "#68D391", "Overweight": "#FBD0AD", "Obesity Class I": "#F9AF78", 
    "Obesity Class II": "#F58342", "Obesity Class III (Morbid)": "#E34813"
}
# --- Fin Constantes ---


# --- Layout de la Página de Resultados ---
def layout(**kwargs): 
    # Este print se ejecutará cada vez que se renderice el layout de esta página
    print(f"DEBUG (results.py layout): INICIO de layout(). kwargs: {kwargs}")
    
    # Importante: El dcc.Store que actúa como INPUT para el callback de esta página
    # NO SE COLOCA AQUÍ en el layout. Se define en la página de predicción como OUTPUT.
    # Aquí solo necesitamos el contenedor donde el callback pondrá los resultados.

    layout_content = html.Div(className="page-container-style", children=[
        html.H1("Your Evaluation Results", className="app-title mb-4"),
        
        # Este Row es el target de nuestro callback. Se inicializa vacío o con un placeholder.
        dbc.Row(
            id="results-content-row", 
            children=[
                dbc.Col(html.P("Loading results, please wait...", id="results-loading-placeholder")) # Placeholder inicial
            ], 
            className="align-items-stretch mb-4"
        ),
        
        dbc.Row(
            dbc.Col(
                dcc.Link(
                    dbc.Button("Perform New Assessment", id="new-eval-button-results", 
                               color="secondary", outline=True, size="lg", className="w-100"),
                    href="/prediction-form" # Asegúrate que este path sea correcto
                ),
            width={"size": 8, "offset": 2}
            )
        )
    ])
    print(f"DEBUG (results.py layout): FIN de layout(). Se devuelve el contenido.")
    return layout_content

# --- Callback para actualizar la página de resultados CON LOS DATOS DEL STORE ---
@callback(
    Output('results-content-row', 'children'), # El Output es el contenido del dbc.Row
    Input('prediction-data-store', 'data'),   # Input: LEE del dcc.Store que tiene id='prediction-data-store'
    prevent_initial_call=False                # ¡Poner en False para que se ejecute al cargar la página!
)
def update_results_page(stored_data): # Renombrado el argumento para claridad
    print(f"DEBUG (results.py callback *update_results_page*): Callback disparado. Data recibida del store: {type(stored_data)}")
    if stored_data:
        print(f"    Contenido del store (primeras 3 claves si es dict): {str(dict(list(stored_data.items())[:3])) if isinstance(stored_data, dict) else str(stored_data)[:200]}...")

    if stored_data is None:
        print("DEBUG (results.py callback): No data in store. Mostrando mensaje de 'No data'.")
        return [dbc.Col(dbc.Alert("No prediction data available. Please perform an assessment first.", 
                                 color="warning-custom", className="text-center"))]

    try:
        prediction_label_raw = stored_data.get('prediction', "N/A")
        confidence = stored_data.get('confidence')
        bmi_value = float(stored_data.get('bmi', 0.0))
        tip_header = stored_data.get('tip_header', "Recommendations")
        tip_text = stored_data.get('tip_text', "Consult a healthcare professional for personalized advice.")
        
        display_label = READABLE_PREDICTION_MAP.get(prediction_label_raw, prediction_label_raw)
        
        header_bg_color = 'var(--color-primary-light)'; header_text_color = 'var(--color-text-primary)';
        if "Obesity" in display_label: header_bg_color = 'var(--color-primary-dark)'; header_text_color = 'white';
        elif "Overweight" in display_label: header_bg_color = 'var(--color-primary)'
        elif "Normal" in display_label: header_bg_color = '#68D391' # Un verde bonito
        elif "Insufficient" in display_label or "Underweight" in display_label : header_bg_color = '#FBD0AD' # Naranja claro


        prediction_card_content = dbc.Card(className="h-100 shadow-sm", children=[
            dbc.CardHeader(html.H5("Your Assessment Summary", className="m-0 text-center fw-bold"), style={'backgroundColor': header_bg_color, 'color': header_text_color, 'borderBottom': '1px solid rgba(0,0,0,0.05)'}),
            dbc.CardBody([
                html.Div([html.Strong("Diagnosis: "), html.Span(display_label, className="fw-bold fs-5", style={'color': 'var(--color-primary-dark)'})], className="mb-2"),
                html.Div([html.Strong("Calculated BMI: "), html.Span(f"{bmi_value:.2f}", className="fw-bold")], className="mb-2"),
                html.Div([html.Strong("Prediction Confidence: "), html.Span(f"{confidence:.1%}" if confidence is not None else "Not Available")], className="mb-3 text-muted small"),
                html.Hr(className="my-3"),
                html.H6(tip_header, className="mt-3 mb-2 fw-bold", style={'color': 'var(--color-primary-dark)'}),
                html.P(tip_text, className="mb-0"),
            ], className="p-4")
        ])
        
        current_bmi_category_name = "Normal Weight" 
        for category, (low, high) in BMI_RANGES.items():
            if low <= bmi_value < high:
                current_bmi_category_name = category
                break
        if bmi_value >= BMI_RANGES["Obesity Class III (Morbid)"][0]:
            current_bmi_category_name = "Obesity Class III (Morbid)"
            
        gauge_bar_color = BMI_COLORS.get(current_bmi_category_name, "#BFBFBF")

        fig_bmi = go.Figure(go.Indicator(
            mode = "gauge+number+delta", value = round(bmi_value, 2),
            delta = {'reference': 22.5, 'increasing': {'color': BMI_COLORS["Overweight"]}, 'decreasing':{'color': BMI_COLORS["Normal Weight"]}, 'font':{'size':12}},
            title = {'text': "Body Mass Index", 'font': {'size': 16, 'color': 'var(--color-text-secondary)'}},
            number= {'font': {'size': 40, 'color': gauge_bar_color, 'family': "Nunito Sans, sans-serif"}, 'valueformat': ".2f"},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [10, 55], 'tickwidth': 1, 'tickcolor': "darkgray", 'tickfont':{'size':10}},
                'bar': {'color': gauge_bar_color, 'thickness': 0.35},
                'bgcolor': "rgba(255,255,255,0.7)", 'borderwidth': 1.5, 'bordercolor': "rgba(0,0,0,0.1)",
                'steps': [
                    {'range': list(BMI_RANGES["Underweight (Severe)"]), 'color': BMI_COLORS["Underweight (Severe)"]},
                    {'range': list(BMI_RANGES["Underweight (Moderate)"]), 'color': BMI_COLORS["Underweight (Moderate)"]},
                    {'range': list(BMI_RANGES["Underweight (Mild)"]), 'color': BMI_COLORS["Underweight (Mild)"]},
                    {'range': list(BMI_RANGES["Normal Weight"]), 'color': BMI_COLORS["Normal Weight"]},
                    {'range': list(BMI_RANGES["Overweight"]), 'color': BMI_COLORS["Overweight"]},
                    {'range': list(BMI_RANGES["Obesity Class I"]), 'color': BMI_COLORS["Obesity Class I"]},
                    {'range': list(BMI_RANGES["Obesity Class II"]), 'color': BMI_COLORS["Obesity Class II"]},
                    {'range': list(BMI_RANGES["Obesity Class III (Morbid)"]), 'color': BMI_COLORS["Obesity Class III (Morbid)"]}
                ],
                 'threshold' : {'line': {'color': "#555555", 'width': 3}, 'thickness': 0.9, 'value': round(bmi_value,2)}
            }))
        fig_bmi.update_layout(height=320, margin=dict(t=10, b=20, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)', font={'family':"Nunito Sans, sans-serif"})

        bmi_card_content = dbc.Card(className="h-100 shadow-sm", children=[
            dbc.CardBody(dcc.Graph(figure=fig_bmi, config={'displayModeBar': False}), 
                         className="d-flex align-items-center justify-content-center p-1 pt-3") # pt-3 para más espacio arriba del gauge
        ])
        
        print("DEBUG (results.py callback): Contenido generado para la página de resultados.")
        # Devuelve una LISTA de dbc.Col
        return [
            dbc.Col(prediction_card_content, lg=7, md=12, className="mb-4 mb-lg-0 d-flex"), 
            dbc.Col(bmi_card_content, lg=5, md=12, className="d-flex")
        ]

    except Exception as e:
        logging.error(f"Error en display_results_on_page_callback: {e}", exc_info=True)
        print(f"ERROR (results.py callback): Excepción al procesar datos o generar layout: {e}")
        return [dbc.Col(dbc.Alert(f"An error occurred while displaying results. Please try again.", 
                                 color="danger-custom", className="text-center"))]