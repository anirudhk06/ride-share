from django.urls import path, re_path, include

from . import views

urlpatterns = [
    re_path(
        r"^auth/",
        include(
            [
                path("login", views.LoginAPI.as_view()),
                path("register", views.RegisterApi.as_view()),
            ]
        ),
    ),
    path("list", views.UserListAPi.as_view()),
]
