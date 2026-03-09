from django.urls import path
from predictor import views
from django.views.generic import RedirectView  # If you have this

urlpatterns = [
    path('', RedirectView.as_view(url='/data_exploration/'), name='home'),  # Your root redirect (keep if you added it)
    path("data_exploration/", views.data_exploration_view, name="data_exploration"),  # Add / here
    path("regression_analysis/", views.regression_analysis, name="regression_analysis"),  # Add / to others too
    path("classification_analysis/", views.classification_analysis, name="classification_analysis"),
    path("clustering_analysis/", views.clustering_analysis, name="clustering_analysis"),
]