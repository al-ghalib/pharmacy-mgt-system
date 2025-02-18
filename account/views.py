from .models import CustomUser, Organization, OrganizationUser, StatusChoices
from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    OrganizationSerializer,
    OrganizationUserSerializer,
    LoginSerializer,
    RegisterSerializer,
)
from .permissions import IsOrganizationAdmin, IsSuperUser
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied


#### Home Page ###

class Home(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        content = {"message": "Hello, user! Welcome to Pharmacy Management System."}
        return Response(content)



#### Login SignUp ###

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user:
            if not user.is_active:
                return Response(
                    {"error": "Your account is deactivated. Contact support."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "User logged in successfully.",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": {
                        "email": user.email,
                    },
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )


#### User ###

class UserProfileView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user 

class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]
    lookup_field = "uid"

    def get_object(self):
        uid = self.kwargs.get("uid")
        return get_object_or_404(CustomUser, uid=uid)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User updated successfully.", "user": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        instance.status = StatusChoices.REMOVED
        instance.save()
        return Response(
            {"message": "User has been successfully marked as removed."},
            status=status.HTTP_200_OK,
        )


#### Organization ###

class OrganizationListCreateView(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            raise PermissionDenied("Only superusers can create an organization.")
        serializer.save()


class OrganizationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsSuperUser]
    lookup_field = "uid"

    def get_object(self):
        uid = self.kwargs.get("uid")
        return super().get_object()

    def update(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Organization updated successfully.",
                    "organization": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        if not self.request.user.is_superuser:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        instance.status = StatusChoices.REMOVED
        instance.save()
        return Response(
            {"message": f"Organization '{instance.name}' has been marked as removed."},
            status=status.HTTP_200_OK,
        )
    

#### Organization User ###

# class OrganizationUserListCreateView(generics.ListCreateAPIView):
#     serializer_class = OrganizationUserSerializer
#     permission_classes = [IsOrganizationAdmin]

#     def get_queryset(self):
#         user = self.request.user

#         if user.is_superuser:  
#             return OrganizationUser.objects.all()  

#         try:
#             organization_user = OrganizationUser.objects.get(user=user)
#         except OrganizationUser.DoesNotExist:
#             return OrganizationUser.objects.none()  

#         if organization_user.role == "ADMIN":  
#             return OrganizationUser.objects.filter(
#                 organization=organization_user.organization, 
#                 role__in=["SALES", "STOCK_UPDATER"]  
#             ).exclude(status=StatusChoices.REMOVED)

#         return OrganizationUser.objects.none()


#     def create(self, request, *args, **kwargs):
#             user = request.user
#             try:
#                 organization_user = OrganizationUser.objects.get(user=user)
#             except OrganizationUser.DoesNotExist:
#                 return Response(
#                     {"message": "You are not associated with any organization."},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             organization_id = request.data.get("organization_id")

#             if int(organization_id) != organization_user.organization.id:
#                 return Response(
#                     {"message": "You cannot create OrganizationUser for a different organization."},
#                     status=status.HTTP_403_FORBIDDEN
#                 )

#             response = super().create(request, *args, **kwargs)
#             return Response(
#                 {"message": "OrganizationUser created successfully.", "data": response.data},
#                 status=status.HTTP_201_CREATED
#             )

class OrganizationUserListCreateView(generics.ListCreateAPIView):
    serializer_class = OrganizationUserSerializer
    permission_classes = [IsOrganizationAdmin]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return OrganizationUser.objects.all()

        organization_user = OrganizationUser.objects.filter(user=user).first()
        if not organization_user:
            return OrganizationUser.objects.none()

        if organization_user.role == "ADMIN":
            return OrganizationUser.objects.filter(
                organization=organization_user.organization,
                role__in=["SALES", "STOCK_UPDATER"]
            ).exclude(status=StatusChoices.REMOVED)

        return OrganizationUser.objects.none()


    def create(self, request, *args, **kwargs):
        user = request.user

        if user.is_superuser:
            return super().create(request, *args, **kwargs)

        try:
            organization_user = OrganizationUser.objects.get(user=user)
        except OrganizationUser.DoesNotExist:
            return Response(
                {"message": "You are not associated with any organization."},
                status=status.HTTP_400_BAD_REQUEST
            )

        organization_id = request.data.get("organization_id")
        if int(organization_id) != organization_user.organization.id:
            return Response(
                {"message": "You cannot create an OrganizationUser for a different organization."},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().create(request, *args, **kwargs)


class OrganizationUserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrganizationUserSerializer
    permission_classes = [IsOrganizationAdmin]
    lookup_field = "uid"

    def get_queryset(self):
        return OrganizationUser.objects.all()  

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if not request.user.is_superuser and not instance.organization_user.user == request.user:
            raise PermissionDenied("You do not have permission to delete this user.")
       
        instance.delete()
       
        return Response(
            {"message": "Organization User has been permanently deleted."},
            status=status.HTTP_204_NO_CONTENT  
        )