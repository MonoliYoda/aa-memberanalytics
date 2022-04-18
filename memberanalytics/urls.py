from django.urls import path

from . import views

app_name = "memberanalytics"

urlpatterns = [
    path("", views.index, name="index"),
    path("add_owner", views.add_owner, name="add_owner"),
]
