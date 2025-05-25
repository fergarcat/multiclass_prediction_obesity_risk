# client/pages/home.py
from dash import html, dcc, register_page # register_page debe estar aquí
import dash_bootstrap_components as dbc

# Registro de la página - ASEGÚRATE QUE EL NOMBRE DEL MÓDULO (__name__) SEA CORRECTO
# Y que todos los argumentos estén.
register_page(
    __name__,  # Esto identifica este módulo como una página
    path='/',  # La URL para esta página
    name="Home",  # Nombre para links autogenerados (si los usaras)
    title="Welcome - PredictHealth Clinic" # Título de la pestaña del navegador
)

# La función layout DEBE existir y devolver componentes Dash válidos.
def layout():
    print("DEBUG (home.py): Rendering layout for / (Homepage)")
    return html.Div(className="page-container-style", children=[
        dbc.Row(
            dbc.Col(
                html.Div([
                    html.H1("Welcome to PredictHealth Clinic", className="app-title mb-3 display-4"),
                    html.P(
                        "Your state-of-the-art tool for health risk assessment. "
                        "Utilize our intelligent system for a personalized analysis of your obesity risk "
                        "and receive actionable recommendations for a healthier lifestyle.",
                        className="app-subtitle mb-5 lead",
                    ),
                    dcc.Link(
                        dbc.Button("Start Obesity Risk Assessment", id="start-eval-button", size="lg", className="w-100 shadow-sm"),
                        href="/prediction-form" 
                    ),
                    html.P(
                        "Powered by advanced Machine Learning models to provide you with accurate insights.",
                        className="text-center text-muted mt-5 small fst-italic"
                    )
                ], className="text-center py-5 px-md-4"),
                width=12 
            )
        )
    ])