from rest_framework import serializers
from .models import User, Organization, OrganizationUser
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "uid",
            "email",
            "first_name",
            "last_name",
            "gender",
            "phone",
            "address",
            "role",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["uid", "created_at", "updated_at"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        min_length=4,
        error_messages={
            "min_length": "Password must be at least 4 characters long.",
        },
    )
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "gender",
            "phone",
            "address",
            "role",
            "status"
        ]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Email is already registered.")
        return value



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise ValidationError("Both email and password are required.")

        user = authenticate(email=email, password=password)

        if not user:
            raise ValidationError("Invalid email or password.")

        data["user"] = user
        return data


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "id",
            "uid",
            "name",
            "trade_licence",  
            "phone",
            "email",
            "address",
            "details",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["uid", "created_at", "updated_at"]


class OrganizationUserSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        fullname = serializers.SerializerMethodField()
        class Meta:
            model = User
            fields = ["id", "email", "fullname"]

        def get_fullname(self, obj):
            return f"{obj.first_name} {obj.last_name}".strip() 

    class OrganizationSerializer(serializers.ModelSerializer):
        class Meta:
            model = Organization
            fields = ["id", "name"]


    user = UserSerializer(read_only=True) 
    organization = OrganizationSerializer(read_only=True)
   
    class Meta:
        model = OrganizationUser
        fields = [
            "id",
            "uid",
            "user",
            "organization",
            "role",
            "status",
            "salary",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["uid", "created_at", "updated_at"]
