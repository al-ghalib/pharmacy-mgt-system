from .models import CustomUser, Organization, OrganizationUser, StatusChoices
from .serializers import (
    UserSerializer,
    OrganizationSerializer,
    OrganizationUserSerializer,
    LoginSerializer,
    RegisterSerializer,
)
from .permissions import IsOrganizationAdmin, IsSuperUser
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError


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


class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]
    lookup_field = "uid"

    def perform_destroy(self, instance):
        instance.status = StatusChoices.REMOVED
        instance.save()


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]

    def get_object(self):
        uid = self.kwargs.get("uid")
        return get_object_or_404(CustomUser, uid=uid)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()

        if "email" in data:
            new_email = data["email"]
            if new_email != instance.email:
                if (
                    CustomUser.objects.filter(email=new_email)
                    .exclude(uid=instance.uid)
                    .exists()
                ):
                    return Response(
                        {"email": ["A user with that email already exists."]},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

        serializer = self.get_serializer(instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "User updated successfully.",
                    "user": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]
    lookup_field = "uid"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
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
    permission_classes = [IsSuperUser]


class OrganizationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsSuperUser | IsOrganizationAdmin]
    lookup_field = "uid"

    def perform_destroy(self, instance):
        instance.status = StatusChoices.REMOVED
        instance.save()


class OrganizationUpdateView(generics.UpdateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsSuperUser | IsOrganizationAdmin]
    lookup_field = "uid"

    def update(self, request, *args, **kwargs):
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


class OrganizationDeleteView(generics.DestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsSuperUser]
    lookup_field = "uid"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = StatusChoices.REMOVED
        instance.save()
        return Response(
            {"message": f"Organization '{instance.name}' has been marked as removed."},
            status=status.HTTP_200_OK,
        )



#### Organization User ###

class OrganizationUserListCreateView(generics.ListCreateAPIView):
    serializer_class = OrganizationUserSerializer
    permission_classes = [IsOrganizationAdmin]

    def get_queryset(self):
        return OrganizationUser.objects.exclude(status=StatusChoices.REMOVED)

    def perform_create(self, serializer):
        user = serializer.validated_data["user_id"]
        organization = serializer.validated_data["organization_id"]

        if OrganizationUser.objects.filter(
            user=user, organization=organization
        ).exists():
            raise ValidationError("This user is already a member of the organization.")

        serializer.save()
        return Response(
            {"message": "Organization User created successfully."},
            status=status.HTTP_201_CREATED,
        )


class OrganizationUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrganizationUserSerializer
    permission_classes = [IsOrganizationAdmin]
    lookup_field = "uid"

    def get_queryset(self):
        return OrganizationUser.objects.exclude(status=StatusChoices.REMOVED)

    def perform_destroy(self, instance):
        instance.status = StatusChoices.REMOVED
        instance.save()
        return Response(
            {"message": "Organization User has been marked as removed."},
            status=status.HTTP_200_OK,
        )
