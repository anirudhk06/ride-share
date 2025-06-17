from rest_framework import serializers
from .models import Ride
from django.contrib.auth import get_user_model

USER = get_user_model()


class RideCreateSerializer(serializers.ModelSerializer):
    vehicle_type = serializers.ChoiceField(
        choices=Ride.VehicleType.choices,
    )

    class Meta:
        model = Ride
        fields = [
            "driver",
            "pickup_location",
            "dropoff_location",
            "distance",
            "vehicle_type",
        ]


class RideListSerializer(serializers.ModelSerializer):
    class RiderSerializer(serializers.ModelSerializer):
        class Meta:
            model = USER
            fields = ["username", "phone"]

    rider = RiderSerializer()
    vehicle_type = serializers.CharField(source="get_vehicle_type_display")

    class Meta:
        model = Ride
        fields = [
            "id",
            "rider",
            "pickup_location",
            "dropoff_location",
            "distance",
            "estimated_time_minutes",
            "vehicle_type",
            "created_at",
            "updated_at",
        ]
