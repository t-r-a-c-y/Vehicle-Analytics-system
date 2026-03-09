from django.shortcuts import render
import joblib
import os
import numpy as np

# Get base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load ML model
model_path = os.path.join(
    BASE_DIR,
    "model_generators",
    "classification",
    "classification_model.pkl"
)

classification_model = joblib.load(model_path)


# -----------------------------
# Data Exploration Page
# -----------------------------
def data_exploration_view(request):

    return render(request, "data_exploration.html")


# -----------------------------
# Prediction Page
# -----------------------------
def predict_view(request):

    prediction = None

    if request.method == "POST":

        bill_length = float(request.POST["bill_length"])
        bill_depth = float(request.POST["bill_depth"])
        flipper_length = float(request.POST["flipper_length"])
        body_mass = float(request.POST["body_mass"])

        features = np.array([[bill_length, bill_depth, flipper_length, body_mass]])

        prediction = classification_model.predict(features)[0]

    return render(request, "predict.html", {"prediction": prediction})
