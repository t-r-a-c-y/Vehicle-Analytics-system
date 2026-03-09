import pandas as pd
from django.shortcuts import render
from predictor.data_exploration import dataset_exploration, data_exploration

def data_exploration_view(request):
    df = pd.read_csv("dummy-data/vehicles_ml_dataset.csv")

    context = {
        "data_exploration": data_exploration(df),
        "dataset_exploration": dataset_exploration(df),
    }

    return render(request, "predictor/index.html", context)

def regression_analysis(request):
    return render(request, "predictor/regretion_analysis.html")

def classification_analysis(request):
    return render(request, "predictor/classification_analysis.html")

def clustering_analysis(request):
    return render(request, "predictor/clustering_analysis.html")
