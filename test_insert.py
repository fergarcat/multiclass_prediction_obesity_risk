from client.services.queries import insert_user_input
from client.config.fields_config import get_field_data

if __name__ == "__main__":
    data = {
        2: 'Male',               # Gender
        3: 35,                   # Age
        6: 'yes',                # family_history_with_overweight
        7: 'no',                 # FAVC
        8: 2.5,                  # FCVC
        9: 3,                    # NCP
        10: 1,                   # CAEC
        12: 3.0,                 # CH2O
        14: 1.2,                 # FAF
        15: 0.5,                 # TUE
        16: 2.0,                 # CALC
        19: 27.5                  # BMI
        # Omito 18 (NObeyesdad) porque es el target (predicción)
    }

    try:
        insert_user_input(data)
        print("Inserción exitosa")
    except Exception as e:
        print(f"Error en inserción: {e}")
