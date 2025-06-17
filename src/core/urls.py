from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(
        r"^api/v1/",
        include(
            [
                re_path(
                    r"^users/",
                    include("apps.users.urls"),
                ),
            ]
        ),
    ),
]
