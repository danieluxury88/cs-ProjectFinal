from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("load_csv", views.load_csv, name="load_csv")
]