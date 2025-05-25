from dash import dcc, html, Input, Output, State, callback, register_page
import dash_bootstrap_components as dbc
from client.config.client_settings import client_settings

register_page(__name__, path='/results', name="Prediction Results", title="Results - PredictHealth")

def layout():
    return html.Div(className="page-container-style", children=[
        html.H1("Prediction Results", className="app-title"),
        html.Div(id='results-content', className="results-content-style"),
        dcc.Store(id='prediction-data-store')
    ])

@callback(
    Output('results-content', 'children'),
    Input('prediction-data-store', 'data')
)
def display_results(data):
    if not data:
        return dbc.Alert("No prediction data available. Please complete the prediction form first.", color="warning")

    # Asumiendo que data tiene keys y valores correctos
    prediction_raw = data.get('prediction', 'Unknown')
    readable_map = {
        "Insufficient_Weight": "Insufficient Weight", "Normal_Weight": "Normal Weight", 
        "Overweight_Level_I": "Overweight Level I", "Overweight_Level_II": "Overweight Level II",
        "Obesity_Type_I": "Obesity Type I", "Obesity_Type_II": "Obesity Type II", "Obesity_Type_III": "Obesity Type III"
    }
    prediction_readable = readable_map.get(prediction_raw, prediction_raw)

    result_elements = [
        html.H3("Prediction Outcome"),
        html.P(f"Risk Category: {prediction_readable}", className="prediction-category"),
        html.Hr()
    ]

    # Puedes mostrar aquí más detalles si vienen en data
    # Por ejemplo, data.get('probabilities'), data.get('input_features') etc.
    if 'probabilities' in data:
        result_elements.append(html.H5("Probabilities:"))
        for k, v in data['probabilities'].items():
            result_elements.append(html.P(f"{k}: {v}"))

    return dbc.Card(dbc.CardBody(result_elements), className="result-card-style")
