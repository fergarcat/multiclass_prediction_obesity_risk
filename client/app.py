# client/app.py
import dash
import dash_bootstrap_components as dbc
from client.components.input_form import create_input_form_layout
from client.callbacks.form_callbacks import register_callbacks

# Inicializa tu app Dash con un tema de Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define el layout de la aplicación
app.layout = create_input_form_layout()

# Registra todos los callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)