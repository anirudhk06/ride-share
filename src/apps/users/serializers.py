from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.db import transaction
from django.db import IntegrityError

USER = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        error_messages={
            "required": "Please enter the email",
            "null": "Please enter the email.",
            "blank": "Please enter the email.",
            "invalid": "Please enter valid email.",
        }
    )
    password = serializers.CharField(
        error_messages={
            "required": "Please enter the password",
            "null": "Please enter the password.",
            "blank": "Please enter the password.",
        }
    )


class UserRegisterSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.fields["confirm_password"] = serializers.CharField(write_only=True)

    password = serializers.CharField(write_only=True)

    class Meta:
        model = USER
        fields = (
            "email",
            "username",
            "firstname",
            "lastname",
            "phone",
            "password",
            "is_driver",
        )

    def validate_phone(self, value) -> str:
        if not str(value).isdigit():
            raise ValueError("Invalid phone number")
        return value

    def validate(self, attrs: dict) -> dict:
        self.fields.pop("confirm_password", None)
        password: str = attrs.get("password")
        confirm_password: str = attrs.pop("confirm_password", None)

        if password != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": "Password is not matching."}
            )

        user = USER(**attrs)

        try:
            validate_password(password, user)
        except ValidationError as e:
            error = serializers.as_serializer_error(e)
            raise serializers.ValidationError({"password": error.get("errors", "")})

        return super().validate(attrs)

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            raise ValueError("Cannot create user")
        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = USER.objects.create_user(**validated_data)
        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = [
            "id",
            "email",
            "username",
            "fullname",
            "phone",
            "is_bot",
            "created_at",
            "updated_at",
        ]


class ProfileSerializer(serializers.ModelSerializer):
    timezone = serializers.CharField(source="user_timezone")

    class Meta:
        model = USER
        fields = [
            "id",
            "email",
            "username",
            "firstname",
            "lastname",
            "phone",
            "is_driver",
            "timezone",
            "created_at",
            "updated_at",
        ]

        read_only_fields = fields
