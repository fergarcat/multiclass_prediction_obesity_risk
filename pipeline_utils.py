import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler

# --- DEFINICIONES DE CLASES Y FUNCIONES ---
# (Estas son las que tu .pkl serializado "recuerda" y necesita encontrar)

# Define the row-level data transformer
class CustomRowTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if not isinstance(X, pd.DataFrame):
            pass
        return X.apply(self._transform_csv_row, axis=1)

    def _transform_csv_row(self, row: pd.Series) -> pd.Series:
        try:
            row['Age'] = int(row['Age'])
        except (ValueError, TypeError):
            # Decide un valor por defecto o cómo manejar el error si la conversión falla
            # Podrías reemplazar con np.nan y que un Imputer lo maneje después, o un valor por defecto.
            row['Age'] = 0
        # Asumir que Height y Weight siempre están presentes y son numéricos
        # Sería bueno añadir manejo de errores aquí también
        height_m = row['Height']
        weight_kg = row['Weight']
        if pd.notna(height_m) and pd.notna(weight_kg) and height_m > 0:
            row['BMI'] = round(weight_kg / (height_m ** 2), 2)
        else:
            row['BMI'] = np.nan # O un valor por defecto

        yes_no_cols = ['family_history_with_overweight', 'FAVC', 'SCC', 'SMOKE'] # Añadí SMOKE si es yes/no
        for col in yes_no_cols:
            if col in row: # Verificar si la columna existe en la fila (DataFrame de entrada)
                val = str(row[col]).strip().lower()
                if val == 'yes':
                    row[col] = 1
                elif val == 'no':
                    row[col] = 0
                else:
                    row[col] = 0 # O np.nan si prefieres imputar luego
            # else: # Si la columna no existe, ¿qué hacer? Podrías crearla con un default o np.nan

        if 'Gender' in row:
            row['Gender'] = 1 if str(row['Gender']).strip().lower() == 'male' else 0

        # Campos numéricos que se convierten a int, asegurarse de manejar NaN o errores
        cols_to_int = ['FCVC', 'NCP']
        for col in cols_to_int:
            if col in row and pd.notna(row[col]):
                try:
                    row[col] = int(row[col])
                except ValueError:
                    row[col] = 0 # O np.nan
            # else: # si falta la columna o es NaN

        if 'CH2O' in row and pd.notna(row['CH2O']):
            try:
                row['CH2O'] = int(float(row['CH2O']) * 100) # Cuidado con multiplicar NaN
            except ValueError:
                row['CH2O'] = 0 # o np.nan
        # else: ...

        cols_to_float_then_int = ['FAF', 'TUE'] # TUE se multiplicaba por 60
        for col in cols_to_float_then_int:
            if col in row and pd.notna(row[col]):
                try:
                    val = float(row[col])
                    if col == 'TUE':
                        val = val * 60
                    row[col] = int(val)
                except ValueError:
                    row[col] = 0 # o np.nan
            # else: ...

        return row

# Define the global preprocessing logic (SOLO LA FUNCIÓN)
def final_processing(df_input: pd.DataFrame) -> pd.DataFrame:
    df = df_input.copy()

    object_cols_to_encode = []
    for col in df.select_dtypes(include='object').columns:
        if col != 'NObeyesdad' and col in object_cols_to_encode:
            try:
                df[col] = df[col].astype('category').cat.codes
            except Exception as e:
                print(f"Advertencia: No se pudo codificar {col}: {e}")
                # df[col] = -1 # o np.nan o algún valor por defecto

    # Convert boolean columns to integers (si las tienes)
    for col in df.select_dtypes(include='bool').columns:
        df[col] = df[col].astype(int)

    # Encode the target variable (esto no debería hacerse en el pipeline de PREPROCESAMIENTO
    # si solo estás transformando features para PREDICCIÓN. El target 'y' no se pasa)
    # if 'NObeyesdad' in df.columns:
    #     df['NObeyesdad'] = df['NObeyesdad'].astype('category').cat.codes

    # Log-transform selected numeric columns
    # Asegurarse de que las columnas existen y son numéricas antes de transformar
    log_transform_cols = ['Weight', 'BMI', 'CH2O', 'FAF', 'TUE']
    for col in log_transform_cols:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            # np.log1p maneja NaN correctamente (devuelve NaN), pero no negativos o no numéricos
            df[col] = np.log1p(df[col].astype(float).clip(lower=0)) # clip para evitar log de negativos
        # else: # Columna no existe o no es numérica

    numerical_cols = ['Age', 'Height', 'Weight', 'BMI', 'CH2O', 'FAF', 'TUE']
    # Por ahora, para que no falle, lo comento o lo hago pasar
    print("ADVERTENCIA: StandardScaler en final_processing está usando fit_transform, lo cual es incorrecto para predicción si no es el mismo scaler que en el entrenamiento.")
    # Si no tienes el scaler entrenado guardado, esto es un problema mayor en tu pipeline.
    # Temporalmente, para que no rompa, podrías hacer esto, pero no es lo ideal:
    existing_numerical_cols = [col for col in numerical_cols if col in df.columns and pd.api.types.is_numeric_dtype(df[col])]
    if existing_numerical_cols:
         temp_scaler = StandardScaler()
         df[existing_numerical_cols] = temp_scaler.fit_transform(df[existing_numerical_cols])

    return df