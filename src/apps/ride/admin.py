from django.contrib import admin
from .models import Ride
# Register your models here.



@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = [
        "driver__username",
        "rider__username",
        "status"
    ]
