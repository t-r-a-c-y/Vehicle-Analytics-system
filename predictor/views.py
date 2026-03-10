import pandas as pd
from django.shortcuts import render
from predictor.data_exploration import dataset_exploration, data_exploration, generate_rwanda_map, generate_world_map  # Add generate_world_map
from model_generators.regression.train_regression import evaluate_regression_model
from model_generators.classification.train_classifier import evaluate_classification_model
from model_generators.clustering.train_cluster import evaluate_clustering_model
import joblib

# Load models
regression_model = joblib.load("model_generators/regression/regression_model.pkl")
classification_model = joblib.load("model_generators/classification/classification_model.pkl")
clustering_model = joblib.load("model_generators/clustering/clustering_model.pkl")

def data_exploration_view(request):
    df = pd.read_csv("dummy-data/vehicles_ml_dataset.csv")
    context = {
        "data_exploration": data_exploration(df),
        "dataset_exploration": dataset_exploration(df),
        "rwanda_map": generate_rwanda_map(df),
        "world_map": generate_world_map(df),  # Add this
    }
    return render(request, "predictor/index.html", context)

# ... rest of the views (regression_analysis, etc.) remain the same ...