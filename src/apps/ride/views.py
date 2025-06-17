from django.http import HttpRequest
from django.utils import timezone
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
)
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response

from .models import Ride
from .serializers import RideCreateSerializer, RideListSerializer
from .permissions import IsDriver


class RequestRideAPI(CreateAPIView):
    serializer_class = RideCreateSerializer
    queryset = Ride.objects.all()

    def create(self, request: HttpRequest, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(rider=request.user)

        return Response(
            {"message": "Request send successfully"}, status=status.HTTP_201_CREATED
        )


class RideListApi(ListAPIView):
    serializer_class = RideListSerializer
    permission_classes = [IsDriver]

    def list(self, request: HttpRequest, *args, **kwargs):
        self.queryset = Ride.objects.filter(
            driver__isnull=True, status=Ride.Status.REQUESTED
        ).exclude(rider=request.user)
        return super().list(self, *args, **kwargs)


class RideRetriveApi(RetrieveUpdateDestroyAPIView):
    serializer_class = RideListSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def retrieve(self, request: HttpRequest, *args, **kwargs):
        self.queryset = Ride.objects.exclude(rider=request.user)
        return super().retrieve(self, *args, **kwargs)


class AcceptRide(RetrieveAPIView):
    lookup_field = "id"
    lookup_url_kwarg = "id"
    permission_classes = [IsDriver]

    def post(self, request: HttpRequest, *args, **kwargs):
        self.queryset = Ride.objects.filter(
            status=Ride.Status.REQUESTED, driver__isnull=True
        ).exclude(rider=request.user)

        obj: Ride = self.get_object()
        obj.driver = request.user
        obj.status = Ride.Status.ACCEPTED
        obj.save()

        return Response({"message": "Success"})


class CancelRide(RetrieveAPIView):
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def post(self, request: HttpRequest, *args, **kwargs):
        self.queryset = Ride.objects.exclude(
            status__in=[Ride.Status.COMPLETED, Ride.Status.CANCELLED],
            rider=request.user,
        )

        reason = request.data.get("reason", None)

        obj: Ride = self.get_object()
        obj.status = Ride.Status.CANCELLED
        obj.cancelled_reason = reason
        obj.save()

        return Response({"message": "Success"})


class StartRide(RetrieveAPIView):
    lookup_field = "id"
    lookup_url_kwarg = "id"
    permission_classes = [IsDriver]

    def post(self, request: HttpRequest, *args, **kwargs):
        self.queryset = Ride.objects.filter(status=Ride.Status.ACCEPTED).exclude(
            rider=request.user
        )

        obj: Ride = self.get_object()
        obj.driver = request.user
        obj.status = Ride.Status.ONGOING
        obj.start_at = timezone.now()
        obj.save()

        return Response({"message": "Ride started"})


class EndRide(RetrieveAPIView):
    lookup_field = "id"
    lookup_url_kwarg = "id"
    permission_classes = [IsDriver]

    def post(self, request: HttpRequest, *args, **kwargs):
        self.queryset = Ride.objects.filter(status=Ride.Status.ONGOING).exclude(
            rider=request.user
        )

        obj: Ride = self.get_object()
        obj.driver = request.user
        obj.status = Ride.Status.COMPLETED
        obj.end_at = timezone.now()
        obj.estimated_time_minutes = (
            abs((obj.start_at - obj.end_at).total_seconds()) / 60
        )
        obj.save()

        return Response({"message": "Ride completed"})
