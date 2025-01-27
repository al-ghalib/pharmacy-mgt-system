# from rest_framework import generics
# from .models import User, Organization, OrganizationUser
# from .serializers import UserSerializer, OrganizationSerializer, OrganizationUserSerializer
# from .permissions import IsAdminOrReadOnly


# class UserListCreateView(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAdminOrReadOnly]  

# class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAdminOrReadOnly]


# class OrganizationListCreateView(generics.ListCreateAPIView):
#     queryset = Organization.objects.all()
#     serializer_class = OrganizationSerializer
#     permission_classes = [IsAdminOrReadOnly]

# class OrganizationDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Organization.objects.all()
#     serializer_class = OrganizationSerializer
#     permission_classes = [IsAdminOrReadOnly]


# class OrganizationUserListCreateView(generics.ListCreateAPIView):
#     queryset = OrganizationUser.objects.all()
#     serializer_class = OrganizationUserSerializer
#     permission_classes = [IsAdminOrReadOnly]

# class OrganizationUserDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = OrganizationUser.objects.all()
#     serializer_class = OrganizationUserSerializer
#     permission_classes = [IsAdminOrReadOnly]


from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import User, Organization, OrganizationUser
from .serializers import UserSerializer, OrganizationSerializer, OrganizationUserSerializer
from .permissions import IsAdminOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]  

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self):
        user_uuid = self.kwargs['pk']
        return get_object_or_404(User, uid=user_uuid)

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self):
        user_uuid = self.kwargs['pk']
        return get_object_or_404(User, uid=user_uuid)

    def perform_destroy(self, instance):
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrganizationListCreateView(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAdminOrReadOnly]


class OrganizationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self):
        org_uuid = self.kwargs['pk']
        return get_object_or_404(Organization, uid=org_uuid)

class OrganizationDeleteView(generics.DestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self):
        org_uuid = self.kwargs['pk']
        return get_object_or_404(Organization, uid=org_uuid)

    def perform_destroy(self, instance):
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrganizationUserListCreateView(generics.ListCreateAPIView):
    queryset = OrganizationUser.objects.all()
    serializer_class = OrganizationUserSerializer
    permission_classes = [IsAdminOrReadOnly]

class OrganizationUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrganizationUser.objects.all()
    serializer_class = OrganizationUserSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self):
        org_user_uuid = self.kwargs['pk']
        return get_object_or_404(OrganizationUser, uid=org_user_uuid)
