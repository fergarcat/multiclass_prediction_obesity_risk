from client.services.queries import get_field_data

def get_fields_config():
    columns = get_field_data()

    return {
        col: {
            "label": col.replace("_", " ").capitalize(),
            "type": "select" if col in ['gender', 'family_history_with_overweight', 'FAVC', 'CAEC', 'SCC', 'CALC'] else (
                     "number" if col in ['age', 'height', 'weight', 'FCVC', 'NCP', 'CH2O', 'FAF', 'TUE'] else "text"),
            "options": ['yes', 'no'] if col in ['FAVC', 'SCC', 'family_history_with_overweight']
                       else ['Male', 'Female'] if col == 'gender'
                       else ['no', 'Sometimes', 'Frequently', 'Always'] if col in ['CAEC', 'CALC']
                       else None
        }
        for col in columns if col != "id"
    }
