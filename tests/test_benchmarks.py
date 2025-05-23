import unittest
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from data.modeling.benchmarks import custom_ml_benchmarks

class TestCustomMLBenchmarks(unittest.TestCase):

    def setUp(self):
        # Create a sample dataset for testing
        self.X = pd.DataFrame({
            'feature1': np.arange(10),
            'feature2': np.arange(10, 20),
            'feature3': np.arange(100, 110)
        })
        self.y = pd.Series([0, 1] * 5)

        # Define a sample models dictionary
        self.models_dict = {
            "Logistic Regression": Pipeline([
                ('scaler', StandardScaler()),
                ('classifier', LogisticRegression(max_iter=1000))
            ])
        }

    def test_custom_ml_benchmarks_output(self):
        # Run the custom_ml_benchmarks function
        results_df = custom_ml_benchmarks(self.X, self.y, self.models_dict)

        # Check if the output is a DataFrame
        self.assertIsInstance(results_df, pd.DataFrame)

        # Check if the DataFrame contains the expected columns
        expected_columns = ['Model', 'Accuracy', 'Precision', 'Recall', 'F1-Score', 'Train Time (s)', 'Overfitting']
        self.assertTrue(all(col in results_df.columns for col in expected_columns))

        # Check if the DataFrame contains results for the provided model
        self.assertIn("Logistic Regression", results_df['Model'].values)

    def test_custom_ml_benchmarks_metrics(self):
        # Run the custom_ml_benchmarks function
        results_df = custom_ml_benchmarks(self.X, self.y, self.models_dict)

        # Check if the metrics are within valid ranges
        for metric in ['Accuracy', 'Precision', 'Recall', 'F1-Score']:
            self.assertTrue((results_df[metric] >= 0).all() and (results_df[metric] <= 1).all())

        # Check if train time and overfitting are non-negative
        self.assertTrue((results_df['Train Time (s)'] >= 0).all())
        self.assertTrue((results_df['Overfitting'] >= -1).all())

if __name__ == "__main__":
    unittest.main()