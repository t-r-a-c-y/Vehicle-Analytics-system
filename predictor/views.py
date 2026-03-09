import pandas as pd
import json
import plotly.express as px
import joblib
import os
from django.shortcuts import render
from .data_exploration import dataset_exploration, data_exploration
from model_generators.regression.train_regression import evaluate_regression_model
from model_generators.classification.train_classifier import evaluate_classification_model
from model_generators.clustering.train_cluster import evaluate_clustering_model

# Load models safely
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
regression_model = joblib.load(os.path.join(BASE_DIR, "regression_model.pkl"))
classification_model = joblib.load(os.path.join(BASE_DIR, "classification_model.pkl"))
clustering_model = joblib.load(os.path.join(BASE_DIR, "model_generators/clustering/clustering_model.pkl"))

def data_exploration_view(request):
    df = pd.read_csv("dummy-data/vehicles_ml_dataset.csv")
    
    # --- UPDATED MAP LOGIC ---
    geojson_path = os.path.join(BASE_DIR, "dummy-data/rwanda_districts.geojson")
    
    if os.path.exists(geojson_path):
        try:
            with open(geojson_path) as f:
                rwanda_geojson = json.load(f)
            
            # Aggregate data by district
            district_counts = df['district'].value_counts().reset_index()
            district_counts.columns = ['district', 'client_count']

            fig = px.choropleth(
                district_counts, 
                geojson=rwanda_geojson, 
                locations="district",
                featureidkey="properties.shapeName", # Standard key for Rwanda GeoJSON
                color="client_count",
                color_continuous_scale="Viridis",
                labels={'client_count': 'Number of Clients'}
            )
            
            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
            map_html = fig.to_html(full_html=False)
        except Exception as e:
            map_html = f"<div class='alert alert-warning'>Map Error: {str(e)}</div>"
    else:
        map_html = "<div class='alert alert-danger'>Missing File: 'rwanda_districts.geojson' not found in dummy-data/</div>"

    context = {
        "dataset_exploration": dataset_exploration(df),
        "data_exploration": data_exploration(df),
        "map_plot": map_html,
    }
    return render(request, "predictor/index.html", context)

def regression_analysis(request):
    context = {"evaluations": evaluate_regression_model()}
    if request.method == "POST":
        year = int(request.POST["year"])
        km = float(request.POST["km"])
        seats = int(request.POST["seats"])
        income = float(request.POST["income"])
        # Ensure input matches model's expected shape
        prediction = regression_model.predict([[year, km, seats, income]])[0]
        context["price"] = prediction
    return render(request, "predictor/regression_analysis.html", context)

def classification_analysis(request):
    context = {"evaluations": evaluate_classification_model()}
    if request.method == "POST":
        year = int(request.POST["year"])
        km = float(request.POST["km"])
        seats = int(request.POST["seats"])
        income = float(request.POST["income"])
        prediction = classification_model.predict([[year, km, seats, income]])[0]
        context["prediction"] = prediction
    return render(request, "predictor/classification_analysis.html", context)

def clustering_analysis(request):
    evals = evaluate_clustering_model()
    df = pd.read_csv("dummy-data/vehicles_ml_dataset.csv")
    
    # Exercise (b): Coefficient of Variation
    cv = round((df['selling_price'].std() / df['selling_price'].mean()) * 100, 2)
    evals['cv'] = cv
    
    context = {"evaluations": evals}
    if request.method == "POST":
        year = int(request.POST["year"])
        km = float(request.POST["km"])
        seats = int(request.POST["seats"])
        income = float(request.POST["income"])
        
        # 1. Predict Price 2. Predict Cluster based on Income and Price
        price_pred = regression_model.predict([[year, km, seats, income]])[0]
        cluster_id = clustering_model.predict([[income, price_pred]])[0]
        
        mapping = {0: "Economy", 1: "Standard", 2: "Premium"}
        context.update({
            "prediction": mapping.get(cluster_id, "Unknown Segment"), 
            "price": price_pred
        })
    return render(request, "predictor/clustering_analysis.html", context)

# In predictor/views.py
from .data_exploration import dataset_exploration, data_exploration, get_rwanda_map

def data_exploration_view(request):
    df = pd.read_csv("dummy-data/vehicles_ml_dataset.csv")

    context = {
        "dataset_exploration": dataset_exploration(df),
        "data_exploration": data_exploration(df),
        "map_plot": get_rwanda_map(df), 
    }

    return render(request, "predictor/index.html", context)
