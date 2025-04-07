# app/ml/model_loader.py

import joblib
import numpy as np
import os

# Define absolute path to model.pkl stored in /app/ml/
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

# Load the model pipeline components
try:
    model_artifacts = joblib.load(MODEL_PATH)
    model = model_artifacts["model"]
    scaler = model_artifacts["scaler"]
    poly = model_artifacts["poly"]
    selector = model_artifacts["selector"]
except Exception as e:
    raise RuntimeError(f"❌ Failed to load model pipeline: {e}")


def predict_diabetes(input_data: dict) -> int:
    """
    Applies preprocessing steps and returns prediction label (0 = Non-Diabetic, 1 = Diabetic)
    """

    try:
        # Convert input to numpy array
        input_array = np.array([[ 
            input_data["pregnancies"],
            input_data["glucose"],
            input_data["blood_pressure"],
            input_data["skin_thickness"],
            input_data["insulin"],
            input_data["bmi"],
            input_data["diabetes_pedigree_function"],
            input_data["age"]
        ]])

        # Preprocessing pipeline
        transformed = poly.transform(input_array)
        scaled = scaler.transform(transformed)
        selected = selector.transform(scaled)

        # Prediction
        prediction = model.predict(selected)
        return int(prediction[0])

    except Exception as e:
        raise RuntimeError(f"❌ Prediction pipeline failed: {e}")
