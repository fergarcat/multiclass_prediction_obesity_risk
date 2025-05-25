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

import optuna
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from xgboost import XGBClassifier
from sklearn.metrics import make_scorer, f1_score
from tabulate import tabulate  


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


def custom_ml_benchmarks(X, y, models_dict, test_size=0.2, random_state=42):
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    import pandas as pd
    import time
    from tabulate import tabulate

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    results = []

    for name, pipeline in models_dict.items():
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




def optimize_xgboost(X, y, n_trials=30, test_size=0.2, random_state=42):
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import accuracy_score
    import optuna
    from xgboost import XGBClassifier

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    # Objective function for Optuna
    def objective(trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 50, 300),
            'max_depth': trial.suggest_int('max_depth', 3, 10),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
            'subsample': trial.suggest_float('subsample', 0.5, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
            'gamma': trial.suggest_float('gamma', 0, 5),
            'reg_alpha': trial.suggest_float('reg_alpha', 0, 1),
            'reg_lambda': trial.suggest_float('reg_lambda', 0, 1),
            'use_label_encoder': False,
            'eval_metric': 'mlogloss'
        }

        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', XGBClassifier(**params))
        ])

        pipeline.fit(X_train, y_train)
        preds = pipeline.predict(X_test)
        return accuracy_score(y_test, preds)

    # Run Optuna
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=n_trials)

    # Train final model with best params
    best_params = study.best_params
    best_params.update({'use_label_encoder': False, 'eval_metric': 'mlogloss'})

    optuna_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', XGBClassifier(**best_params))
    ])

    optuna_pipeline.fit(X_train, y_train)

    # Print summary table
    import time
    from sklearn.metrics import precision_score, recall_score, f1_score
    from tabulate import tabulate

    y_pred = optuna_pipeline.predict(X_test)
    train_pred = optuna_pipeline.predict(X_train)

    train_acc = accuracy_score(y_train, train_pred)
    test_acc = accuracy_score(y_test, y_pred)
    overfitting = train_acc - test_acc

    results = [{
        'Model': 'XGBoost (Optuna)',
        'Accuracy': test_acc,
        'Precision': precision_score(y_test, y_pred, average='weighted'),
        'Recall': recall_score(y_test, y_pred, average='weighted'),
        'F1-Score': f1_score(y_test, y_pred, average='weighted'),
        'Overfitting': round(overfitting, 4)
    }]


    # Return everything needed
    return optuna_pipeline, study, results, X_train, X_test, y_train, y_test
    
