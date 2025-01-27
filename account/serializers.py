from rest_framework import serializers
from .models import User, Organization, OrganizationUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uid', 'email', 'first_name', 'last_name', 'phone', 'address', 'gender', 'image', 'status', 'organization']


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['uid', 'name', 'phone', 'email', 'address', 'trade_licence', 'details', 'branch']


class OrganizationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationUser
        fields = ['uid', 'user', 'organization', 'role', 'status', 'salary']
