from dash import dcc, html, Input, Output, State, callback, register_page, no_update
import dash_bootstrap_components as dbc
import logging
import json 
import plotly.graph_objects as go

register_page(
    __name__, 
    path='/results', 
    name="Results", 
    title="Your Evaluation Results - PredictHealth"
)

READABLE_PREDICTION_MAP = {
    "Insufficient_Weight": "Insufficient Weight", "Normal_Weight": "Normal Weight", 
    "Overweight_Level_I": "Overweight Level I", "Overweight_Level_II": "Overweight Level II",
    "Obesity_Type_I": "Obesity Type I", "Obesity_Type_II": "Obesity Type II", "Obesity_Type_III": "Obesity Type III"
}
BMI_RANGES = {
    "Underweight (Severe)": (0, 15.99), "Underweight (Moderate)": (16, 16.99), "Underweight (Mild)": (17, 18.49),
    "Normal Weight": (18.5, 24.99), "Overweight": (25, 29.99),
    "Obesity Class I": (30, 34.99), "Obesity Class II": (35, 39.99), "Obesity Class III (Morbid)": (40, 100) 
}
BMI_COLORS = { 
    "Underweight (Severe)": "#FBD0AD", "Underweight (Moderate)": "#F9AF78", "Underweight (Mild)": "#F58342",   
    "Normal Weight": "#68D391", "Overweight": "#FBD0AD", "Obesity Class I": "#F9AF78", 
    "Obesity Class II": "#F58342", "Obesity Class III (Morbid)": "#E34813"
}

def layout(**kwargs): 
    print(f"DEBUG (results.py layout): Layout para /results renderizado. kwargs: {kwargs}")
    return html.Div(className="page-container-style", children=[
        dbc.Container([
            html.H1("Your Evaluation Results", className="app-title text-center my-4 display-5 fw-bold"),
            
            dbc.Row(
                id="results-dynamic-content", 
                children=[
                    dbc.Col(dcc.Loading(
                        type="default", 
                        children=html.P("Awaiting prediction data...", id="results-initial-placeholder", className="text-center fst-italic text-muted py-5")
                    ), width=14, className="mb-4 mb-lg-0"),
                ], 
                className="g-lg-4 mb-5 mt-3 align-items-stretch justify-content-center" 
            ),
            
            dbc.Row(
                dbc.Col(
                    dcc.Link(
                        dbc.Button("Perform New Assessment", id="new-eval-button-results-page",
                                   color="primary", outline=False, size="lg", className="w-100 shadow"),
                        href="/prediction-form" 
                    ),
                width={"size": 10, "offset": 1, "md": {"size": 8, "offset": 2}, "lg": {"size": 6, "offset": 3}}
                ), className="mb-5 text-center" 
            )
        ], fluid=False, className="py-4")
    ])

@callback(
    Output('results-dynamic-content', 'children'),
    Input('prediction-data-store', 'data'), 
    Input('app-url', 'pathname'),          
    prevent_initial_call=False             
)
def update_results_content(stored_data, current_pathname):
    print(f"DEBUG (results.py callback 'update_results_content'): Disparado.")
    print(f"    Current Pathname: {current_pathname}")
    print(f"    Data from Store ('prediction-data-store') type: {type(stored_data)}")

    if current_pathname != '/results':
        print("    Pathname NO es /results. Devolviendo no_update.")
        return no_update

    if stored_data is None or not isinstance(stored_data, dict) or not stored_data:
        print("    No hay datos válidos en el store (None, no es dict, o vacío). Mostrando 'sin datos'.")
        return [dbc.Col(dbc.Alert("No prediction data currently available. Please perform an assessment first.", 
                                 color="warning", className="text-center shadow-sm"))]

    print(f"    Datos del Store encontrados. Contenido parcial: {str(dict(list(stored_data.items())[:3]))}...")

    try:
        prediction_label_raw = stored_data.get('prediction', "N/A")
        confidence_value = stored_data.get('confidence')
        bmi_value_from_store = stored_data.get('bmi')

        try:
            bmi_value = float(bmi_value_from_store) if bmi_value_from_store is not None else 0.0
        except (ValueError, TypeError):
            bmi_value = 0.0
            
        tip_header_from_backend = stored_data.get('tip_header', "General Health Advice")
        tip_text_from_backend = stored_data.get('tip_text', "Consistency in healthy habits is key. For specific guidance, consult with a healthcare professional.")
        
        display_label = READABLE_PREDICTION_MAP.get(prediction_label_raw, prediction_label_raw)

        header_bg_color_map = {
            "Obesity": "var(--bs-danger-bg-subtle)", "Overweight": "var(--bs-warning-bg-subtle)",
            "Normal": "var(--bs-success-bg-subtle)", "Insufficient": "var(--bs-info-bg-subtle)", 
            "Underweight": "var(--bs-info-bg-subtle)"
        }
        header_text_color_map = {
             "Obesity": "var(--bs-danger-text-emphasis)", "Overweight": "var(--bs-warning-text-emphasis)",
            "Normal": "var(--bs-success-text-emphasis)", "Insufficient": "var(--bs-info-text-emphasis)", 
            "Underweight": "var(--bs-info-text-emphasis)"
        }
        header_bg_color = 'var(--bs-secondary-bg-subtle)'; header_text_color = 'var(--bs-secondary-text-emphasis)';
        for key_word, color_val_bg in header_bg_color_map.items():
            if key_word in display_label:
                header_bg_color = color_val_bg
                header_text_color = header_text_color_map.get(key_word, 'var(--bs-body-color)')
                break
        
        prediction_card_body_content = [
            html.Div([
                html.Strong("Diagnosis:", className="text-muted"), 
                html.Span(display_label, className="fw-bolder fs-4 ms-2", style={'color': header_text_color}) # Usa el color de texto del header
            ], className="mb-3 text-center"),
            html.Div([
                html.Strong("Calculated BMI: ", className="text-muted"), 
                html.Span(f"{bmi_value:.2f} kg/m²", className="fw-bold fs-5")
            ], className="mb-2 text-center"),
            html.Div([
                html.Strong("Prediction Confidence: ", className="text-muted"), 
                html.Span(f"{confidence_value:.1%}" if confidence_value is not None else "Not Available", className="fw-bold")
            ], className="mb-4 text-center small"),
            html.Hr(className="my-4"),
            html.H5(tip_header_from_backend, className="mb-3 fw-bold text-primary text-center"), 
            html.P(tip_text_from_backend, className="mb-0 text-secondary text-center", style={'fontSize': '1rem'}),
        ]

        prediction_card = dbc.Card(
            [
                dbc.CardHeader(html.H4("Assessment Summary", className="m-0 text-center fw-bold"), 
                               style={'backgroundColor': header_bg_color, 'color': header_text_color}),
                dbc.CardBody(prediction_card_body_content, className="p-4")
            ], className="h-100 shadow-lg border-0 mb-4 mb-lg-0"
        )
        
        current_bmi_category_name = "Normal Weight" 
        for category_name_iter, (low, high) in BMI_RANGES.items():
            if low <= bmi_value <= high: current_bmi_category_name = category_name_iter; break
        if bmi_value > BMI_RANGES["Obesity Class III (Morbid)"][1]: current_bmi_category_name = "Obesity Class III (Morbid)"
        gauge_bar_color = BMI_COLORS.get(current_bmi_category_name, "#BFBFBF")

        fig_bmi = go.Figure(go.Indicator(
            mode = "gauge+number", 
            value = round(bmi_value, 2),
            title = {'text': "Body Mass Index (BMI)", 'font': {'size': 18, 'color': 'var(--bs-body-color)'}},
            number= {'font': {'size': 48, 'color': gauge_bar_color, 'family': "Arial Black, sans-serif"}, 'valueformat': ".2f"},
            domain = {'x': [0, 1], 'y': [0.05, 0.95]},
            gauge = {
                'axis': {'range': [10, 55], 'tickwidth': 1, 'tickcolor': "darkgray", 'tickfont':{'size':10}},
                'bar': {'color': gauge_bar_color, 'thickness': 0.3},
                'bgcolor': "rgba(255,255,255,0.8)", 'borderwidth': 1, 'bordercolor': "rgba(0,0,0,0.1)",
                'steps': [ # Sin cambios aquí
                    {'range': BMI_RANGES["Underweight (Severe)"], 'color': BMI_COLORS["Underweight (Severe)"]},
                    {'range': BMI_RANGES["Underweight (Moderate)"], 'color': BMI_COLORS["Underweight (Moderate)"]},
                    {'range': BMI_RANGES["Underweight (Mild)"], 'color': BMI_COLORS["Underweight (Mild)"]},
                    {'range': BMI_RANGES["Normal Weight"], 'color': BMI_COLORS["Normal Weight"]},
                    {'range': BMI_RANGES["Overweight"], 'color': BMI_COLORS["Overweight"]},
                    {'range': BMI_RANGES["Obesity Class I"], 'color': BMI_COLORS["Obesity Class I"]},
                    {'range': BMI_RANGES["Obesity Class II"], 'color': BMI_COLORS["Obesity Class II"]},
                    {'range': BMI_RANGES["Obesity Class III (Morbid)"], 'color': BMI_COLORS["Obesity Class III (Morbid)"]}
                ],
                'threshold' : {'line': {'color': "#333", 'width': 3}, 'thickness': 0.85, 'value': round(bmi_value,2)}
            }))
        fig_bmi.update_layout(
            height=280,
            margin=dict(t=30, b=10, l=30, r=30),
            paper_bgcolor='rgba(0,0,0,0)',
            font={'family':"Arial, sans-serif"}
        )

        bmi_card = dbc.Card([
             dbc.CardHeader(html.H5("BMI Visualizer", className="m-0 text-center fw-bold"),
                            style={'backgroundColor': 'var(--bs-light)', 'color': 'var(--bs-dark)'}),
             dbc.CardBody(dcc.Graph(figure=fig_bmi, config={'displayModeBar': False, 'responsive': True},
                                    ), 
                          className="d-flex align-items-center justify-content-center p-md-3 p-2")
            ], className="h-100 shadow-lg border-0"
        )
        
        print("DEBUG (results.py callback): Contenido de tarjetas y gráfico generado para /results.")
        return [
            dbc.Col(prediction_card, width=12, lg=30, className="mb-4 mb-lg-0"),
            dbc.Col(bmi_card, width=12, lg=30)
        ]

    except Exception as e:
        logging.error(f"Error en results.py (update_results_content): {e}", exc_info=True)
        return [dbc.Col(dbc.Alert(f"An error occurred displaying results: {str(e)}", 
                                 color="danger", className="text-center"))]