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
