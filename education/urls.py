from django.urls import path
from . import views

app_name = "education"

urlpatterns = [
    path("", views.training_list, name="training_list"),
    path("<slug:slug>/", views.training_detail, name="training_detail"),
]
