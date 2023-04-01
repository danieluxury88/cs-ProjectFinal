from django.urls import path
from . import views

urlpatterns = [

    path("", views.index, name="index"),

    # API URLS

    path("profile/<int:profile_id>", views.profile, name="profile"),
    path("register/<int:profile_id>", views.register, name="register"),

    #tests
    path("test", views.test, name="test"),
    path("owners", views.owners_list, name="owners"),
    path("owners/<str:city>", views.owners_by_city, name="owners_by_city"),
    path("owners/model/<str:model>", views.owners_by_model, name="owners_by_model"),
    
    
    path("load_csv", views.load_csv, name="load_csv"),
    path("data_cleaner/<int:option>", views.data_cleaner, name="data_cleaner"),

]