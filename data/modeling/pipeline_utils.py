
#Load libraries
import pandas as pd
import numpy as np
from sklearn.metrics import mutual_info_score
from scipy.stats import chi2_contingency
import os
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler
import numpy as np
import pandas as pd
import joblib

# Define the row-level data transformer
class CustomRowTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.apply(self._transform_csv_row, axis=1)

    def _transform_csv_row(self, row):
        row['Age'] = int(row['Age'])

        height_m = row['Height']
        weight_kg = row['Weight']
        row['BMI'] = round(weight_kg / (height_m ** 2), 2)

        yes_no_cols = ['family_history_with_overweight', 'FAVC', 'SCC']
        for col in yes_no_cols:
            val = str(row[col]).strip().lower()
            if val == 'yes':
                row[col] = 1
            elif val == 'no':
                row[col] = 0
            else:
                row[col] = 0  # Treat any other value as "no"

        row['Gender'] = 1 if str(row['Gender']).strip().lower() == 'male' else 0

        row['FCVC'] = int(row['FCVC'])
        row['NCP'] = int(row['NCP'])
        row['CH2O'] = int(float(row['CH2O']) * 100)
        row['FAF'] = int(float(row['FAF']))
        row['TUE'] = int(float(row['TUE']) * 60)

        return row

# Define the global preprocessing logic
def final_processing(df):
    df = df.copy()

    # Encode non-target object columns
    for col in df.select_dtypes(include='object').columns:
        if col != 'NObeyesdad':
            df[col] = df[col].astype('category').cat.codes

    # Convert boolean columns to integers
    for col in df.select_dtypes(include='bool').columns:
        df[col] = df[col].astype(int)

    # Encode the target variable
    if 'NObeyesdad' in df.columns:
        df['NObeyesdad'] = df['NObeyesdad'].astype('category').cat.codes

    # Log-transform selected numeric columns
    log_transform_cols = ['Weight', 'BMI', 'CH2O', 'FAF', 'TUE']
    for col in log_transform_cols:
        df[col] = np.log1p(df[col])

    # Standardize numerical features
    numerical_cols = ['Age', 'Height', 'Weight', 'BMI', 'CH2O', 'FAF', 'TUE']
    df[numerical_cols] = StandardScaler().fit_transform(df[numerical_cols])

    return df

# Define the full preprocessing pipeline
full_pipeline = Pipeline(steps=[
    ('row_cleaning', CustomRowTransformer()),
    ('final_processing', FunctionTransformer(final_processing))
])

# Define paths
csv_file_name = "train.csv"
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)

csv_file_path = os.path.join(parent_dir, ".kaggle", csv_file_name)
pre_pkl_file_name = "preprocessing_pipeline.pkl"
pre_pkl_path = os.path.join(parent_dir, "modeling", "pkl", pre_pkl_file_name)

# Load the raw dataset
df_original = pd.read_csv(csv_file_path)

# Fit the pipeline to the data
full_pipeline.fit(df_original)

# Save the pipeline as a .pkl file
joblib.dump(full_pipeline, pre_pkl_path)

print(f"✅ Preprocessing pipeline saved to: {pre_pkl_path}")
