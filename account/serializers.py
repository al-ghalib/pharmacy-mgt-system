from rest_framework import serializers
from .models import CustomUser, Organization, OrganizationUser
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "uid",
            "email",
            "first_name",
            "last_name",
            "gender",
            "phone",
            "address",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["uid", "created_at", "updated_at"]


class UserDetailSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "fullname",
        ]
        read_only_fields = ["id", "fullname"]

    def get_fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()



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
        model = CustomUser
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "gender",
            "phone",
            "address",
            "status"
        ]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
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


class OrganizationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
        ]
        read_only_fields = ["id", "name"]



class OrganizationUserSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    organization = OrganizationDetailSerializer(read_only=True)

    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), write_only=True
    )
    organization_id = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(), write_only=True
    )

    class Meta:
        model = OrganizationUser
        fields = [
            "id",
            "uid",
            "user",
            "user_id",  
            "organization",
            "organization_id",  
            "role",
            "status",
            "salary",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["uid", "created_at", "updated_at"]

    def create(self, validated_data):
        user = validated_data.pop("user_id")
        organization = validated_data.pop("organization_id")
        
        if OrganizationUser.objects.filter(user=user, organization=organization).exists():
            raise serializers.ValidationError(
                {"detail": "This user is already a member of the organization."}
            )

        return OrganizationUser.objects.create(user=user, organization=organization, **validated_data)

