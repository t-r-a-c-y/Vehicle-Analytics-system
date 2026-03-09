from django.urls import path
from predictor import views
from . import views

urlpatterns = [
    path("data_exploration", views.data_exploration_view, name="data_exploration"),
]

