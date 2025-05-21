import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

from tabulate import tabulate  # pip install tabulate


def ml_benchmarks(X, y, test_size=0.2, random_state=42):

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    classifiers = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Decision Tree": DecisionTreeClassifier(),
        "Random Forest": RandomForestClassifier(),
        "SVM (Linear)": SVC(kernel='linear'),
        "SVM (RBF)": SVC(kernel='rbf'),
        "Naive Bayes": GaussianNB(),
        "KNN": KNeighborsClassifier(),
        "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss'),
        "LightGBM": LGBMClassifier(),
        "CatBoost": CatBoostClassifier(verbose=0)
    }

    results = []

    for name, clf in classifiers.items():
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', clf)
        ])

        start_time = time.time()
        pipeline.fit(X_train, y_train)
        train_time = time.time() - start_time

        y_train_pred = pipeline.predict(X_train)
        y_test_pred = pipeline.predict(X_test)

        train_acc = accuracy_score(y_train, y_train_pred)
        test_acc = accuracy_score(y_test, y_test_pred)
        overfitting = train_acc - test_acc

        results.append({
            'Model': name,
            'Accuracy': test_acc,
            'Precision': precision_score(y_test, y_test_pred, average='weighted', zero_division=0),
            'Recall': recall_score(y_test, y_test_pred, average='weighted', zero_division=0),
            'F1-Score': f1_score(y_test, y_test_pred, average='weighted', zero_division=0),
            'Train Time (s)': round(train_time, 4),
            'Overfitting': round(overfitting, 4)
        })

    results_df = pd.DataFrame(results).sort_values(by='F1-Score', ascending=False)

    print(tabulate(results_df, headers='keys', tablefmt='pretty', showindex=False))

    return results_df
