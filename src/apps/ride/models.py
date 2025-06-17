from django.db import models
from django.contrib.auth import get_user_model

from db.mixins import AuditModel

# Create your models here.

USER = get_user_model()


class Ride(AuditModel):
    class Status(models.TextChoices):
        REQUESTED = "requested", "Requested"
        ACCEPTED = "accepted", "Accepted"
        ONGOING = "ongoing", "Ongoing"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    class VehicleType(models.TextChoices):
        CAR = "car", "Car"
        BIKE = "bike", "Bike"
        AUTO = "auto", "Auto"

    driver = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="drives", null=True)
    rider = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="rides")
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    start_at = models.DateTimeField(null=True)
    end_at = models.DateTimeField(null=True)
    distance = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    estimated_time_minutes = models.PositiveIntegerField(null=True, blank=True)

    cancelled_reason = models.TextField(blank=True, null=True)

    vehicle_type = models.CharField(
        max_length=20, choices=VehicleType.choices, default=VehicleType.CAR
    )
    status = models.CharField(
        max_length=100, choices=Status.choices, default=Status.REQUESTED
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Ride {self.id} | {self.rider} → {self.dropoff_location}"
