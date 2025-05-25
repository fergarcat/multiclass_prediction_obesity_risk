# client/app.py
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.SANDSTONE],
    use_pages=True,
    suppress_callback_exceptions=True,
    title="Keep In Shape App - Obesity Risk Assessment"
)
server = app.server

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Start Prediction", href="/prediction-form")),
        dbc.NavItem(dbc.NavLink("Results", href="/results")),
    ],
    brand="Keep In Shape App",
    brand_href="/",
    color="primary", 
    dark=True,
    sticky="top",
    className="mb-4 shadow-sm" 
)

footer = html.Footer(
    dbc.Container(
        dbc.Row(dbc.Col(html.P(f"© {pd.Timestamp.now().year} Keep In Shape App. All rights reserved.", className="text-center small text-muted"))),
        fluid=True,
        className="py-3 mt-auto"
    ),
    className="footer-custom bg-light border-top"
)

app.layout = html.Div([
    dcc.Location(id='app-url', refresh=False),
    dcc.Store(id='prediction-data-store', storage_type='session'), 
    navbar,
    html.Div(
        dash.page_container,
        id='page-content-wrapper',
        className="flex-grow-1"
    ),
    footer
], id="app-main-layout", style={'display': 'flex', 'flexDirection': 'column', 'minHeight': '100vh'})

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)