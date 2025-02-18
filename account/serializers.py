from rest_framework import serializers
from .models import CustomUser, Organization, OrganizationUser
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
import re


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

    def validate_email(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError("Enter a valid email address.")
        if CustomUser.objects.filter(email=value).exclude(uid=self.instance.uid).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def validate_phone(self, value):
        if not re.match(r"^\+?[1-9]\d{1,14}$", value):  
            raise serializers.ValidationError("Enter a valid phone number.")
        if CustomUser.objects.filter(phone=value).exclude(uid=self.instance.uid).exists():
            raise serializers.ValidationError("A user with that phone number already exists.")
        return value

    def validate_status(self, value):
        valid_statuses = ['ACTIVE', 'INACTIVE', 'REMOVED']
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Status must be one of {valid_statuses}.")
        return value

    def validate(self, attrs):
        return attrs


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


class UserProfileSerializer(serializers.ModelSerializer):
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

    # def validate_email(self, value):
    #     if CustomUser.objects.filter(email=value).exists():
    #         raise ValidationError("Email is already registered.")
    #     return value
    
    def validate_email(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError("Enter a valid email address.")
        
        existing_user = CustomUser.objects.filter(email=value)
        if self.instance:
            existing_user = existing_user.exclude(uid=self.instance.uid) 
        
        if existing_user.exists():
            raise serializers.ValidationError("A user with that email already exists.")
        
        return value

    # def validate_phone(self, value):
    #     if not re.match(r"^\+?[1-9]\d{1,14}$", value):  
    #         raise serializers.ValidationError("Enter a valid phone number.")
    #     if CustomUser.objects.filter(phone=value).exclude(uid=self.instance.uid).exists():
    #         raise serializers.ValidationError("A user with that phone number already exists.")
    #     return value

    def validate_phone(self, value):
        if not re.match(r"^\+?[1-9]\d{1,14}$", value):  
            raise serializers.ValidationError("Enter a valid phone number.")
        
        existing_user = CustomUser.objects.filter(phone=value)
        
        if self.instance:
            existing_user = existing_user.exclude(uid=self.instance.uid)

        if existing_user.exists():
            raise serializers.ValidationError("A user with that phone number already exists.")
        
        return value


    def validate_status(self, value):
        valid_statuses = ['ACTIVE', 'INACTIVE', 'REMOVED']
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Status must be one of {valid_statuses}.")
        return value

    def validate(self, attrs):
        return attrs



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

    def validate_name(self, value):
        if Organization.objects.filter(name=value).exists():
            raise serializers.ValidationError("An organization with this name already exists.")
        return value

    def validate_email(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError("Enter a valid email address.")
        if Organization.objects.filter(email=value).exists():
            raise serializers.ValidationError("An organization with this email already exists.")
        return value

    def validate_phone(self, value):
        if not re.match(r"^\+?[1-9]\d{1,14}$", value):  
            raise serializers.ValidationError("Enter a valid phone number.")
        if Organization.objects.filter(phone=value).exists():
            raise serializers.ValidationError("An organization with this phone number already exists.")
        return value

    def validate_status(self, value):
        valid_statuses = ['ACTIVE', 'INACTIVE', 'REMOVED']
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Status must be one of {valid_statuses}.")
        return value

    def validate(self, attrs):
        return attrs


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


    # def create(self, validated_data):
    #     user = validated_data.pop("user_id")
    #     organization = validated_data.pop("organization_id")
    #     if OrganizationUser.objects.filter(user=user, organization=organization).exists():
    #         raise serializers.ValidationError(
    #             {"non_field_errors": ["This user is already a member of the organization."]}
    #         )
    #     return OrganizationUser.objects.create(user=user, organization=organization, **validated_data)

    # def validate(self, attrs):
    #     user = attrs.get("user_id")
    #     if OrganizationUser.objects.filter(user=user).exists():
    #         raise serializers.ValidationError(
    #             {"non_field_errors": ["This user already has a role in another organization."]}
    #         )
    #     return attrs

    def validate(self, attrs):
        user = attrs.get("user_id")
        organization = attrs.get("organization_id")
        role = attrs.get("role")
        request_user = self.context["request"].user

        if OrganizationUser.objects.filter(user=user, organization=organization).exists():
            raise serializers.ValidationError(
                {"non_field_errors": ["This user is already a member of the organization."]}
            )

        if OrganizationUser.objects.filter(user=user).exclude(organization=organization).exists():
            raise serializers.ValidationError(
                {"non_field_errors": ["This user is already associated with another organization."]}
            )

        if role not in ["SALES", "STOCK_UPDATER"] and not request_user.is_superuser:
            raise serializers.ValidationError(
                {"role": "Only superusers or organization admins can assign other roles."}
            )

        if role == "ADMIN" and not request_user.is_superuser:
            raise serializers.ValidationError(
                {"role": "You cannot assign the ADMIN role unless you are a superuser."}
            )

        salary = attrs.get("salary", 0)
        if salary < 0:
            raise serializers.ValidationError(
                {"salary": "Salary cannot be negative."}
            )

        return attrs

    def create(self, validated_data):
        user = validated_data.pop("user_id")
        organization = validated_data.pop("organization_id")

        if OrganizationUser.objects.filter(user=user, organization=organization).exists():
            raise serializers.ValidationError(
                {"non_field_errors": ["This user is already a member of the organization."]}
            )

        return OrganizationUser.objects.create(user=user, organization=organization, **validated_data)