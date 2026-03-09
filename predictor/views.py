import os
import pandas as pd
import joblib
from django.shortcuts import render
from django.conf import settings
from predictor.data_exploration import dataset_exploration, data_exploration

# Load your model (ensure you have trained and saved this file first)
# Use an absolute path to find the model file in your project root
MODEL_PATH = os.path.join(settings.BASE_DIR, "classification_model.pkl")

def data_exploration_view(request):
    # Fix: Use settings.BASE_DIR to create an absolute path to your CSV
    csv_path = os.path.join(settings.BASE_DIR, "dummy-data", "vehicles_ml_dataset.csv")
    
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        return render(request, "predictor/index.html", {"error": f"File not found at {csv_path}"})

    context = {
        "data_exploration": data_exploration(df),
        "dataset_exploration": dataset_exploration(df),
    }
    return render(request, "predictor/index.html", context)

def regression_analysis(request):
    # This logic depends on your evaluate_regression_model function
    # Ensure that function is imported or defined here
    context = {
        # "evaluations": evaluate_regression_model() 
    }

    if request.method == "POST":
        try:
            year = int(request.POST["year"])
            km = float(request.POST["km"])
            seats = int(request.POST["seats"])
            income = float(request.POST["income"])

            # Load model and predict
            if os.path.exists(MODEL_PATH):
                model = joblib.load(MODEL_PATH)
                prediction = model.predict([[year, km, seats, income]])[0]
                context["price"] = round(float(prediction), 2)
            else:
                context["error"] = "Model file not found. Please run train_classifier.py first."
        except Exception as e:
            context["error"] = str(e)

    return render(request, "predictor/regression_analysis.html", context)

# Add a placeholder for classification if you have a separate page for it
def classification_analysis(request):
    return render(request, "predictor/classification_analysis.html")

import joblib 
from model_generators.clustering.train_cluster import evaluate_clustering_model 
from model_generators.classification.train_classifier import evaluate_classification_model 
from model_generators.regression.train_regression import evaluate_regression_model 
 
# Load models once 
regression_model = joblib.load("model_generators/regression/regression_model.pkl") 
classification_model = joblib.load("model_generators/classification/classification_model.pkl") 
clustering_model = joblib.load("model_generators/clustering/clustering_model.pkl") 
 
def classification_analysis(request): 
    context = { 
        "evaluations": evaluate_classification_model() 
    } 
    if request.method == "POST": 
        year = int(request.POST["year"]) 
        km = float(request.POST["km"]) 
        seats = int(request.POST["seats"]) 
        income = float(request.POST["income"]) 
        prediction = classification_model.predict([[year, km, seats, income]])[0] 
 
        context["prediction"] = prediction 
    return render(request, "predictor/classification_analysis.html", context) 
 
def clustering_analysis(request): 
    context = { 
        "evaluations": evaluate_clustering_model() 
    } 
    if request.method == "POST": 
        try: 
            year = int(request.POST["year"]) 
            km = float(request.POST["km"]) 
            seats = int(request.POST["seats"]) 
            income = float(request.POST["income"]) 
            # Step 1: Predict price 
            predicted_price = regression_model.predict([[year, km, seats, income]])[0] 
            # Step 2: Predict cluster 
            cluster_id = clustering_model.predict([[income, predicted_price]])[0] 
            mapping = { 
                0: "Economy", 
                1: "Standard", 
                2: "Premium" 
            } 
            context.update({ 
                "prediction": mapping.get(cluster_id, "Unknown"), 
                "price": predicted_price 
            }) 
        except Exception as e: 
            context["error"] = str(e) 
 
    return render(request, "predictor/clustering_analysis.html", context) 