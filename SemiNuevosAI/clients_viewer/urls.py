from django.urls import path
from . import views

urlpatterns = [

    path("", views.index, name="index"),
    path("test", views.test, name="test"),
    path("load_csv", views.load_csv, name="load_csv"),

    # API URLS

    path("profile/", views.profile, name="profile"),

]