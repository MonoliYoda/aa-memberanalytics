from django.urls import path

from . import views

app_name = "memberanalytics"

urlpatterns = [
    path("", views.index, name="index"),
    path("add_owner", views.add_owner, name="add_owner"),
    path("member_details/<int:id>", views.member_details, name="member_details")
]
