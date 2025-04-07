# models/model_training.py

import pandas as pd
import polars as pl
import joblib
import os
import warnings
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.feature_selection import RFECV
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from imblearn.over_sampling import SMOTE
import optuna

warnings.filterwarnings('ignore')

# Load the dataset
df = pl.read_csv("diabetes_updated.csv").to_pandas()
X = df.drop("Outcome", axis=1)
y = df["Outcome"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Preprocessing
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

scaler = StandardScaler()
poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)

X_poly = poly.fit_transform(X_resampled)
X_scaled = scaler.fit_transform(X_poly)

# Feature selection
selector = RFECV(estimator=RandomForestClassifier(), step=1, cv=5, scoring='accuracy', n_jobs=-1)
selector.fit(X_scaled, y_resampled)
X_selected = selector.transform(X_scaled)

# Define base models (no GPU for compatibility)
base_models = [
    ('xgb', XGBClassifier(use_label_encoder=False, eval_metric='logloss')),
    ('lgbm', LGBMClassifier()),
    ('rf', RandomForestClassifier()),
    ('cat', CatBoostClassifier(verbose=0))  # Removed task_type="GPU"
]

# Define stacking model
stacking_model = StackingClassifier(
    estimators=base_models,
    final_estimator=RandomForestClassifier(),
    cv=5,
    n_jobs=-1
)

# Hyperparameter tuning using Optuna
def objective(trial):
    n_estimators = trial.suggest_int('n_estimators', 100, 1000)
    max_depth = trial.suggest_int('max_depth', 3, 20)
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
    model.fit(X_selected, y_resampled)
    return model.score(X_selected, y_resampled)

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=10)

best_params = study.best_params
print("Best Parameters:", best_params)

# Update final model with best params
final_rf = RandomForestClassifier(**best_params)

final_model = StackingClassifier(
    estimators=base_models,
    final_estimator=final_rf,
    cv=5,
    n_jobs=-1
)

# Train final model
final_model.fit(X_selected, y_resampled)

# Ensure 'models' directory exists
os.makedirs("models", exist_ok=True)

# Save model and preprocessors
joblib.dump({
    "model": final_model,
    "scaler": scaler,
    "poly": poly,
    "selector": selector
}, "models/model.pkl")

print("Model training and saving completed successfully!")
