def get_field_data():
    data = {
        "Gender": {"label": "Gender:", "type": "dropdown", "options": ["Male", "Female"], "default": "Male"},
        "Age": {"label": "Age (years):", "type": "number", "default": 25, "min": 1, "max": 99},
        "Height": {"label": "Height (meters):", "type": "number", "default": 1.7, "min": 1.0, "max": 2.5},
        "Weight": {"label": "Weight (kg):", "type": "number", "default": 70.0, "min": 30.0, "max": 200.0},
        "Family_History_with_Overweight": {"label": "Family history with overweight:", "type": "dropdown", "options": ["yes", "no"], "default": "yes"},
        "FAVC": {"label": "Frequent consumption of high caloric food:", "type": "dropdown", "options": ["yes", "no"], "default": "yes"},
        "FCVC": {"label": "Frequency of consumption of vegetables (0-3):", "type": "number", "default": 2.0, "min": 0.0, "max": 3.0},
        "NCP": {"label": "Number of main meals (0-4):", "type": "number", "default": 3.0, "min": 0.0, "max": 4.0},
        "CAEC": {"label": "Consumption of food between meals:", "type": "dropdown", "options": ["no", "Sometimes", "Frequently", "Always"], "default": "Sometimes"},
        "SMOKING": {"label": "Smoking:", "type": "dropdown", "options": ["yes", "no"], "default": "no"},
        "CH2O": {"label": "Daily water consumption (liters, 0-3):", "type": "number", "default": 2.0, "min": 0.0, "max": 3.0},
        "SCC": {"label": "Calories consumption monitoring:", "type": "dropdown", "options": ["yes", "no"], "default": "no"},
        "FAF": {"label": "Physical activity frequency (0-3):", "type": "number", "default": 1.0, "min": 0.0, "max": 3.0},
        "TUE": {"label": "Time using technology devices (0-3):", "type": "number", "default": 0.0, "min": 0.0, "max": 3.0},
        "CALC": {"label": "Alcohol consumption:", "type": "dropdown", "options": ["no", "Sometimes", "Frequently", "Always"], "default": "no"},
        "MTRANS": {"label": "Main transportation:", "type": "dropdown", "options": ["Public_Transportation", "Walking", "Automobile", "Bike", "Motorbike"], "default": "Public_Transportation"}
    }
    return data