# client/components/input_form.py
from dash import dcc, html
import dash_bootstrap_components as dbc
from client.config.fields_config import get_field_data

def create_input_form_layout():
    fields = get_field_data()
    print(f"DEBUG (client): Inside create_input_form_layout. fields.keys() are: {list(fields.keys())}") # (Este ya lo tienes)
    
    form_elements = [] # Inicializamos la lista de elementos del formulario.
    print(f"DEBUG (client): Initializing form_elements as empty list.")

    # Iteramos sobre cada campo definido en fields_config.py
    for field_id, config in fields.items(): # Aquí debería iterar sobre los 16 campos
        print(f"DEBUG (client): --- Processing field_id: {field_id}, config: {config}")
        
        input_component = None # Reiniciamos el componente para cada campo.

        if config["type"] == "number":
            print(f"DEBUG (client): Creating dcc.Input (number) for {field_id}")
            input_component = dcc.Input(
                id=f'input-{field_id}',
                type='number',
                value=config["default"],
                min=config.get("min"),
                max=config.get("max"),
                step=config.get("step", 0.1),
                className="form-control"
            )
        elif config["type"] == "dropdown":
            print(f"DEBUG (client): Creating dcc.Dropdown for {field_id}")
            options_list = [{'label': opt, 'value': opt} for opt in config["options"]]
            input_component = dcc.Dropdown(
                id=f'input-{field_id}',
                options=options_list,
                value=config["default"],
                clearable=False
            )
        else:
            print(f"DEBUG (client): Field {field_id} has unknown type: {config.get('type')}")
            
        # Si se generó un input_component (es decir, no fue None), lo añadimos al layout.
        if input_component is not None:
            print(f"DEBUG (client): SUCCESS! Adding component for {field_id} to form_elements.")
            form_elements.append(
                dbc.Row([
                    dbc.Col(dbc.Label(f"{config['label']}:", html_for=f'input-{field_id}'), width=6),
                    dbc.Col(input_component, width=6),
                ], className="mb-3")
            )
        else:
            # Esto no debería pasar si los tipos son 'number' o 'dropdown'
            print(f"DEBUG (client): WARNING! No input_component created for {field_id}. Check its 'type' in fields_config.")

    print(f"DEBUG (client): Finished loop. Number of elements in form_elements: {len(form_elements)}")
    # Si len(form_elements) es 0 o muy bajo, ahí está el problema. Debería ser 16.

    # El layout principal que se devuelve.
    return dbc.Container([
        html.H1("Predicción de Riesgo de Obesidad", className="text-center my-4"),
        html.P("Ingresa los datos para predecir el riesgo de obesidad.", className="text-center text-muted"),

        dbc.Card(dbc.CardBody(form_elements)), # Aquí es donde los form_elements se insertan.
        
        dbc.Button('Realizar Predicción', id='predict-button', n_clicks=0, color="primary", className="my-4 w-100"),
        
        dbc.Alert(id='prediction-output', className="text-center my-2", is_open=False, duration=4000, style={'marginTop': '20px'}),
        dbc.Alert(id='error-output', color="danger", className="text-center my-2", is_open=False, duration=4000),
        
        dcc.Loading(id="loading-output", type="default", children=html.Div(id="loading-div", style={'marginTop': '20px'}))
    ], className="mt-5", style={'maxWidth': '800px'})