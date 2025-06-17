import uuid
import pytz
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone


class User(AbstractBaseUser, PermissionsMixin):
    # choices
    USER_TIMEZONE_CHOICES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    id = models.UUIDField(
        default=uuid.uuid4(),
        unique=True,
        editable=False,
        db_index=True,
        primary_key=True,
    )
    username = models.CharField(max_length=120, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=100, blank=True, default="")
    firstname = models.CharField(max_length=40)
    lastname = models.CharField(max_length=40, blank=True, default="")

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Modified At")

    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    last_active = models.DateTimeField(default=timezone.now, null=True)
    last_login_time = models.DateTimeField(null=True)

    is_bot = models.BooleanField(default=False)

    user_timezone = models.CharField(
        max_length=255, default="UTC", choices=USER_TIMEZONE_CHOICES
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "users"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.pk} <{self.email}>"

    @property
    def fullname(self) -> str:
        return f"{self.firstname} {self.lastname}"
