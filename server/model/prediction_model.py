# server/model/prediction_model.py
import joblib
import pandas as pd
from pydantic import BaseModel, Field
from typing import List, Optional
import numpy as np
import logging

# --- MAPAS DE CONVERSIÓN DEFINITIVOS (para los strings que tu preprocesador no está manejando) ---
# Asegúrate de que los valores numéricos (0, 1, 2, 3) coincidan con lo que tu modelo fue entrenado.
# Si el preprocesador ya convierte alguna (como Gender, FAVC, SCC), este mapa no la afectará si ya son números.
MANUAL_STRING_TO_INT_MAPS = {
    "Family_History_with_Overweight": {"yes": 1, "no": 0},
    "CAEC": {"no": 0, "Sometimes": 1, "Frequently": 2, "Always": 3},
    "SMOKING": {"yes": 1, "no": 0},
    "CALC": {"no": 0, "Sometimes": 1, "Frequently": 2, "Always": 3},
    # MTRANS es más complejo porque tiene muchas categorías. Si tu modelo final lo espera One-Hot Encoded
    # (y el preprocesador no lo hace), tendrías que hacer OHE aquí.
    # Por ahora, vamos a suponer que tu preprocesador debería convertir MTRANS a algo numérico.
    # Si tu preprocesador DEJA MTRANS como string y el modelo final espera números de MTRANS,
    # este es un problema más profundo del preprocesador.
    # Como MTRANS no estaba en `model_pipeline.feature_names_in_`, es posible que tu modelo final no lo use.
    # Pero si lo usa, tu preprocesador debe transformarlo a numérico.
    "MTRANS": { # Ejemplo si necesitas mapearlo; esto es SOLO UN EJEMPLO DE ÚLTIMO RECURSO
        "Public_Transportation": 0, "Walking": 1, "Automobile": 2, "Bike": 3, "Motorbike": 4
    }
}


class PredictionRequest(BaseModel): # SIN CAMBIOS
    Gender: str
    Age: int = Field(..., gt=0, lt=100)
    Height: float = Field(..., gt=1.0, lt=2.5)
    Weight: float = Field(..., gt=30.0, lt=200.0)
    Family_History_with_Overweight: str
    FAVC: str
    FCVC: float = Field(..., gt=0.0, lt=4.0)
    NCP: float = Field(..., gt=0.0, lt=5.0)
    CAEC: str
    SMOKING: str
    CH2O: float = Field(..., gt=0.0, lt=4.0)
    SCC: str
    FAF: float = Field(..., gt=0.0, lt=4.0)
    TUE: float = Field(..., ge=0.0, lt=4.0)
    CALC: str
    MTRANS: str

class PredictionResponse(BaseModel): # SIN CAMBIOS
    prediction: str
    confidence: Optional[float] = None
    bmi: Optional[float] = None
    input_data: PredictionRequest

class ObesityRiskModel:
    def __init__(self, preprocessing_pipeline_path: str, model_pipeline_path: str): # SIN CAMBIOS
        self.preprocessor = self._load_pipeline(preprocessing_pipeline_path)
        self.model = self._load_pipeline(model_pipeline_path)
        logging.info("Modelos (preprocesador y predictor) cargados exitosamente.")

        # Basado en tu inspección, el modelo final espera estas. MTRANS fue eliminado.
        self.model_input_columns = [
            'Gender', 'Age', 'Height', 'Weight', 'family_history_with_overweight', 
            'FAVC', 'FCVC', 'NCP', 'CAEC', 'CH2O', 'SCC', 'FAF', 'TUE', 'CALC', 'BMI'
        ]
        logging.info(f"El modelo final (`self.model`) espera las columnas: {self.model_input_columns}")

    def _load_pipeline(self, pipeline_path: str): # SIN CAMBIOS
            try:
                return joblib.load(pipeline_path)
            except Exception as e:
                logging.error(f"Error cargando pipeline desde {pipeline_path}: {e}")
                raise RuntimeError(f"Error cargando pipeline: {e}")

    def calculate_bmi(self, weight_kg: float, height_m: float) -> float: # SIN CAMBIOS
        if height_m <= 0:
            return 0.0
        return weight_kg / (height_m ** 2)

    def predict(self, data: PredictionRequest) -> PredictionResponse:
        input_data_dict_pascal = data.model_dump() if hasattr(data, 'model_dump') else data.dict()
        input_df_for_preprocessor = pd.DataFrame([input_data_dict_pascal])
        
        logging.info(f"DEBUG (server): DF (PascalCase) cols PASSED TO preprocessor.transform(): {input_df_for_preprocessor.columns.tolist()}")
        
        df_after_preprocessor = self.preprocessor.transform(input_df_for_preprocessor)

        if not isinstance(df_after_preprocessor, pd.DataFrame):
            # Intenta crear un DataFrame con los nombres originales + BMI si el preprocesador devuelve NumPy
            # Esto es una suposición fuerte sobre lo que produce el preprocesador
            temp_cols = input_df_for_preprocessor.columns.tolist()
            if "BMI" not in temp_cols and "bmi" not in temp_cols: # Chequea si BMI ya está o se espera que esté
                 if df_after_preprocessor.shape[1] == len(temp_cols) + 1: # Asume BMI es la columna extra
                     temp_cols.append("BMI") # Nómbrala consistentemente
                 else:
                     # Este es un error grave, no podemos adivinar las columnas
                     raise ValueError(f"Preprocessor devolvió NumPy con forma {df_after_preprocessor.shape} pero no se pueden inferir columnas. Originales: {len(temp_cols)}")
            df_after_preprocessor = pd.DataFrame(df_after_preprocessor, columns=temp_cols)
            logging.info(f"DEBUG (server): Preprocessor output (NumPy) convertido a DF. Cols: {df_after_preprocessor.columns.tolist()}")
        else:
            logging.info(f"DEBUG (server): Preprocessor output (DF) ya es DataFrame. Cols: {df_after_preprocessor.columns.tolist()}")

        # --- INICIO DE NUEVA SECCIÓN DE CONVERSIÓN MANUAL ---
        # `df_after_preprocessor` es lo que salió de tu `preprocessing_pipeline.pkl`.
        # Necesitamos asegurar que las columnas que el modelo final espera como numéricas (pero que el
        # preprocesador podría haber dejado como strings) se conviertan aquí.
        # Tu inspección dijo que `self.model` espera `family_history_with_overweight` (snake_case)
        # y el resto en PascalCase (Gender, Age, etc.).
        # `df_after_preprocessor` ya tiene `BMI` añadido por tu preprocesador, y `Gender`, `FAVC`, `SCC`
        # ya son numéricos (0/1) según tu log de "Muestra de datos ANTES de self.model.predict()".

        # Campos que necesitan conversión manual de string a int que el preprocesador no hizo:
        fields_to_manually_convert = {
            # Clave (nombre de columna en df_after_preprocessor) : Mapa a usar
            "Family_History_with_Overweight": MANUAL_STRING_TO_INT_MAPS["Family_History_with_Overweight"],
            "CAEC": MANUAL_STRING_TO_INT_MAPS["CAEC"],
            "SMOKING": MANUAL_STRING_TO_INT_MAPS["SMOKING"],
            "CALC": MANUAL_STRING_TO_INT_MAPS["CALC"],
            "MTRANS": MANUAL_STRING_TO_INT_MAPS["MTRANS"] # Si MTRANS es necesario y el modelo lo espera numérico
        }

        df_for_model_construction = df_after_preprocessor.copy() # Trabaja sobre una copia

        for col_name_pascal, current_map in fields_to_manually_convert.items():
            if col_name_pascal in df_for_model_construction.columns:
                # Solo convierte si la columna todavía es string.
                # Si el preprocesador ya la convirtió a número, .map() no la afectará mal
                # si el mapa solo tiene claves string.
                if df_for_model_construction[col_name_pascal].dtype == 'object': # 'object' usualmente significa string
                    df_for_model_construction[col_name_pascal] = df_for_model_construction[col_name_pascal].map(current_map)
                    logging.info(f"Columna '{col_name_pascal}' convertida manualmente a numérico usando mapa.")
                else:
                    logging.info(f"Columna '{col_name_pascal}' ya es numérica, no se aplica mapa manual.")
            else:
                logging.warning(f"Columna '{col_name_pascal}' no encontrada en la salida del preprocesador para conversión manual.")
        
        # Renombrar 'Family_History_with_Overweight' a 'family_history_with_overweight' (snake_case)
        # porque el modelo final lo espera así.
        if 'Family_History_with_Overweight' in df_for_model_construction.columns:
            df_for_model_construction = df_for_model_construction.rename(
                columns={'Family_History_with_Overweight': 'family_history_with_overweight'}
            )
            logging.info("Columna 'Family_History_with_Overweight' renombrada a 'family_history_with_overweight'.")
        
        # --- FIN DE NUEVA SECCIÓN DE CONVERSIÓN MANUAL ---

        # Seleccionar EXACTAMENTE las columnas que el modelo final espera.
        # `self.model_input_columns` YA está definido en `__init__` con lo que la inspección nos dio.
        try:
            df_for_model = df_for_model_construction[self.model_input_columns]
        except KeyError as e:
            msg = (f"CRITICAL ERROR FINAL: No se pudieron seleccionar las columnas finales para el modelo. "
                   f"Columnas DISPONIBLES después del preprocesador Y CONVERSIÓN MANUAL: {list(df_for_model_construction.columns)}. "
                   f"Columnas REQUERIDAS por `self.model_input_columns`: {self.model_input_columns}. "
                   f"Error específico de KeyError: {e}")
            logging.error(msg)
            raise ValueError(msg) from e
        
        logging.info(f"DEBUG (server): DataFrame cols FINALMENTE PASADAS a self.model.predict(): {df_for_model.columns.tolist()}")
        
        # Este print es crucial para ver si los DATOS son realmente numéricos.
        if not df_for_model.empty:
            print(f"DEBUG (server): Muestra de datos ANTES de self.model.predict() (después de conversión manual):\n{df_for_model.head(1).to_dict(orient='records')}")

        prediction_array = self.model.predict(df_for_model)
        prediction_label = str(prediction_array[0])

        confidence = None
        if hasattr(self.model, 'predict_proba'):
            probabilities = self.model.predict_proba(df_for_model)[0]
            predicted_class_idx = np.argmax(probabilities)
            confidence = probabilities[predicted_class_idx]
            
        bmi_for_response = df_for_model['BMI'].iloc[0] if 'BMI' in df_for_model else self.calculate_bmi(data.Weight, data.Height)

        return PredictionResponse(
            prediction=prediction_label,
            confidence=confidence,
            bmi=bmi_for_response, 
            input_data=data
        )