import unittest
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from data.modeling.pipeline_utils import CustomRowTransformer, final_processing, full_pipeline

class TestPipelineUtils(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame for testing
        self.sample_data = pd.DataFrame({
            'Age': ['25', '30'],
            'Height': [1.75, 1.80],
            'Weight': [70, 80],
            'family_history_with_overweight': ['yes', 'no'],
            'FAVC': ['yes', 'no'],
            'SCC': ['no', 'yes'],
            'Gender': ['male', 'female'],
            'FCVC': ['3', '2'],
            'NCP': ['3', '2'],
            'CH2O': ['2.5', '3.0'],
            'FAF': ['1.0', '0.5'],
            'TUE': ['0.5', '1.0'],
            'NObeyesdad': ['Normal_Weight', 'Overweight_Level_I']
        })

    def test_custom_row_transformer(self):
        transformer = CustomRowTransformer()
        transformed_data = transformer.fit_transform(self.sample_data)

        # Check if the transformation is applied correctly
        self.assertEqual(transformed_data['Age'][0], 25)
        self.assertEqual(transformed_data['BMI'][0], round(70 / (1.75 ** 2), 2))
        self.assertEqual(transformed_data['family_history_with_overweight'][0], 1)
        self.assertEqual(transformed_data['Gender'][0], 1)
        self.assertEqual(transformed_data['CH2O'][0], 250)
        self.assertEqual(transformed_data['TUE'][0], 30)

    def test_final_processing(self):
        self.sample_data['BMI'] = self.sample_data.apply(
            lambda row: round(row['Weight'] / (row['Height'] ** 2), 2),
            axis=1
        )
        processed_data = final_processing(self.sample_data)

        # Check if categorical columns are encoded
        self.assertTrue(np.issubdtype(processed_data['family_history_with_overweight'].dtype, np.integer))
        self.assertTrue(processed_data['NObeyesdad'].dtype.name == 'int8')

        # Check if numerical columns are standardized
        numerical_cols = ['Age', 'Height', 'Weight', 'BMI', 'CH2O', 'FAF', 'TUE']
        
        for col in numerical_cols:
            self.assertAlmostEqual(processed_data[col].mean(), 0, delta=1e-6)
            self.assertAlmostEqual(np.std(processed_data[col], ddof=0), 1, delta=1e-6)


    def test_full_pipeline(self):
        # Fit the pipeline to the sample data
        pipeline = full_pipeline.fit(self.sample_data)
        transformed_data = pipeline.transform(self.sample_data)

        # Check if the pipeline output matches expectations
        self.assertIsInstance(pipeline, Pipeline)
        self.assertEqual(transformed_data.shape[0], self.sample_data.shape[0])  # mismo número de filas
        self.assertGreaterEqual(transformed_data.shape[1], self.sample_data.shape[1])  # igual o más columnas


if __name__ == "__main__":
    unittest.main()