from django.http import HttpRequest
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework import status
from rest_framework.response import Response


from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from rest_framework_simplejwt.tokens import RefreshToken


from .serializers import (
    LoginSerializer,
    UserRegisterSerializer,
    UserListSerializer,
    ProfileSerializer,
)

USER = get_user_model()


class LoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request: HttpRequest, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email: str = serializer.validated_data.get("email")
        password: str = serializer.validated_data.get("password")

        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )

        refresh = RefreshToken.for_user(user)

        return Response({"refresh": str(refresh), "access": str(refresh.access_token)})


class RegisterApi(APIView):
    permission_classes = [AllowAny]

    def post(self, request: HttpRequest, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "detail": "Registration completed successfully",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


class ProfileAPI(RetrieveAPIView):
    serializer_class = ProfileSerializer

    def retrieve(self, request: HttpRequest, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class UserListAPi(ListAPIView):
    queryset = USER.objects.all()
    serializer_class = UserListSerializer

    def list(self, request: HttpRequest, *args, **kwargs):
        return super().list(request, *args, **kwargs)
