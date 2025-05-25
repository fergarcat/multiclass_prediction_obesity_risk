# client/app.py
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd # Para el año del footer

# Inicializa la app Dash
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.SANDSTONE], # O el tema que prefieras
    use_pages=True, # MUY IMPORTANTE
    suppress_callback_exceptions=True, # Recomendado para apps multi-página
    title="PredictHealth Clinic - Obesity Risk Assessment" # Título global de la app
)
server = app.server # Exponer para despliegue

# --- Navbar ---
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")), # Link a la página de inicio
        dbc.NavItem(dbc.NavLink("Start Prediction", href="/prediction-form")),
        # Puedes añadir más páginas aquí después
    ],
    brand="PredictHealth Clinic",
    brand_href="/",
    color="primary", 
    dark=True,
    sticky="top", # Para que se quede fijo
    className="mb-4 shadow-sm" 
)

# --- Footer ---
footer = html.Footer(
    dbc.Container(
        dbc.Row(dbc.Col(html.P(f"© {pd.Timestamp.now().year} PredictHealth Clinic. All rights reserved.", className="text-center small text-muted"))),
        fluid=True,
        className="py-3 mt-auto" # Padding vertical y margen superior automático
    ),
    className="footer-custom bg-light border-top" # bg-light para un footer claro
)

# El layout principal de la aplicación. Contiene dcc.Location y dash.page_container.
app.layout = html.Div([
    dcc.Location(id='app-url', refresh=False), # El router principal de Dash Pages
    navbar,
    html.Div( # Contenedor para el contenido de la página, para aplicar estilos y flex
        dash.page_container,
        id='page-content-wrapper',
        className="flex-grow-1" # Para que este div crezca y empuje el footer
    ),
    footer
], id="app-main-layout", style={'display': 'flex', 'flexDirection': 'column', 'minHeight': '100vh'})


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)