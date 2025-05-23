from dash import Dash, html
import dash_bootstrap_components as dbc
from client.components.input_form import generate_input_fields
from client.callbacks.form_callbacks import register_callbacks
from client.components.input_form import serve_layout

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Análisis de Obesidad"
app._favicon = "media/pics/persimon_logo.png"
app.layout = serve_layout
register_callbacks(app)

app.layout = dbc.Container([
    html.H2("Obesity Prediction Form", className="text-center my-4"),
    generate_input_fields(),
    html.Div(id="submission-status", className="my-3"),
    dbc.Button("Submit", id="submit-button", color="primary", className="w-100"),
    dbc.Row([
            dbc.Col([
                html.Button("Resultado", id='predict-btn', n_clicks=0,
                            style={
                                'marginTop': '10px',
                                'padding': '10px 20px',
                                'backgroundColor': APR_COLOR,
                                'border': 'none',
                                'borderRadius': '12px',
                                'fontSize': '16px',
                                'fontWeight': 'bold',
                                'color': 'white',
                                'width': '100%'
                            },
                            disabled=True)
            ])
        ]),

        dbc.Row([
            dbc.Col([
                html.Div(id='prediction-bubble', style={'marginTop': '20px'})
            ])
        ])
    ], fluid=True)
], style={'backgroundColor': GRAY_BG, 'padding': '10px', 'height': '100vh', 'overflow': 'hidden'})

], fluid=True)

register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True, host="127.0.0.1", port=8050)
