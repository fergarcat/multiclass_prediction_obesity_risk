# client/config/fields_config.py
def get_field_data():
    """
    Este diccionario hardcodeado define **todos los campos de entrada** de la UI y sus propiedades.
    Las claves de este diccionario ('Gender', 'Age', etc.) deben coincidir
    **EXACTAMENTE** con los atributos del PredictionRequest de tu backend (incluyendo MAYÚSCULAS y minúsculas).
    """
    return {
        "Gender": {"label": "Género", "type": "dropdown", "options": ["Male", "Female"], "default": "Male"},
        "Age": {"label": "Edad (años)", "type": "number", "default": 25, "min": 1, "max": 99},
        "Height": {"label": "Altura (metros)", "type": "number", "default": 1.70, "min": 1.0, "max": 2.5},
        "Weight": {"label": "Peso (kg)", "type": "number", "default": 70.0, "min": 30.0, "max": 200.0},
        "Family_History_with_Overweight": {"label": "Historia familiar de sobrepeso", "type": "dropdown", "options": ["yes", "no"], "default": "yes"},
        "FAVC": {"label": "Consumo frecuente de comida alta en calorías", "type": "dropdown", "options": ["yes", "no"], "default": "yes"},
        "FCVC": {"label": "Frecuencia de consumo de vegetales (0-3)", "type": "number", "default": 2.0, "min": 0.0, "max": 3.0},
        "NCP": {"label": "Número de comidas principales (0-4)", "type": "number", "default": 3.0, "min": 0.0, "max": 4.0},
        "CAEC": {"label": "Consumo de alimentos entre comidas", "type": "dropdown", "options": ["no", "Sometimes", "Frequently", "Always"], "default": "Sometimes"},
        "SMOKING": {"label": "Fuma", "type": "dropdown", "options": ["yes", "no"], "default": "no"},
        "CH2O": {"label": "Consumo de agua diario (litros, 0-3)", "type": "number", "default": 2.0, "min": 0.0, "max": 3.0},
        "SCC": {"label": "Monitoreo de consumo de calorías", "type": "dropdown", "options": ["yes", "no"], "default": "no"},
        "FAF": {"label": "Frecuencia de actividad física (0-3)", "type": "number", "default": 1.0, "min": 0.0, "max": 3.0},
        "TUE": {"label": "Tiempo usando dispositivos tecnológicos (0-3)", "type": "number", "default": 0.0, "min": 0.0, "max": 3.0},
        "CALC": {"label": "Consumo de alcohol", "type": "dropdown", "options": ["no", "Sometimes", "Frequently", "Always"], "default": "no"},
        "MTRANS": {"label": "Medio de transporte principal", "type": "dropdown", "options": ["Public_Transportation", "Walking", "Automobile", "Bike", "Motorbike"], "default": "Public_Transportation"}
    }