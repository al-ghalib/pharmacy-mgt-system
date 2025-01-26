from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import User, Organization, OrganizationUser
from .serializers import (
    UserSerializer,
    OrganizationSerializer,
    OrganizationUserSerializer,
)
from .permissions import IsAdminUser


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class OrganizationListCreateView(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class OrganizationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class OrganizationUserListCreateView(generics.ListCreateAPIView):
    queryset = OrganizationUser.objects.all()
    serializer_class = OrganizationUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class OrganizationUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrganizationUser.objects.all()
    serializer_class = OrganizationUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
