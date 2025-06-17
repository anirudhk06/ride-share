from django.http import HttpRequest
from rest_framework.permissions import BasePermission


class IsDriver(BasePermission):

    def has_permission(self, request: HttpRequest, view) -> bool:
        return getattr(request.user, "is_driver", False)
