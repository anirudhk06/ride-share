from django.urls import path
from . import views

urlpatterns = [
    path("request", views.RequestRideAPI.as_view()),
    path("available", views.RideListApi.as_view()),
    path("retrive/<int:id>", views.RideRetriveApi.as_view()),
    path("accept-ride/<int:id>", views.AcceptRide.as_view()),
    path("start-ride/<int:id>", views.StartRide.as_view()),
    path("ride-completed/<int:id>", views.EndRide.as_view()),
    path("cancel-ride/<int:id>", views.CancelRide.as_view()),
]
