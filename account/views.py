from .models import User, Organization, OrganizationUser, StatusChoices
from .serializers import (
    UserSerializer,
    OrganizationSerializer,
    OrganizationUserSerializer,
    LoginSerializer,
    RegisterSerializer,
)
from .permissions import IsAdmin
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication


class Home(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        content = {"message": "Hello, user! Welcome to Pharmacy Management System."}
        return Response(content)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": {
                        "uid": user.uid,
                        "email": user.email,
                    },
                },
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
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "uuid": user.uid,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    lookup_field = "uid"


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    def get_object(self):
        uid = self.kwargs.get("uid")
        return get_object_or_404(User, uid=uid)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()

        if "email" in data:
            new_email = data["email"]
            if new_email != instance.email:
                if (
                    User.objects.filter(email=new_email)
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
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    lookup_field = "uid"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = StatusChoices.REMOVED
        instance.save()
        # instance.delete()
        return Response(
            {"message": "User status updated to removed successfully."},
            status=status.HTTP_200_OK,
        )


class OrganizationListCreateView(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAdmin]


class OrganizationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAdmin]
    lookup_field = "uid"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(f"Updating organization: {instance.name}")
        return super().update(request, *args, **kwargs)


class OrganizationUpdateView(generics.UpdateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAdmin]
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
    permission_classes = [IsAdmin]
    lookup_field = "uid"

    def perform_destroy(self, instance):
        print(f"Deleting Organization: {instance.name}")
        instance.status = "removed"
        instance.save()
        # instance.delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "message": f"Organization '{instance.name}' has been soft-deleted successfully."
            },
            status=status.HTTP_200_OK,
        )


class OrganizationUserListCreateView(generics.ListCreateAPIView):
    queryset = OrganizationUser.objects.all()
    serializer_class = OrganizationUserSerializer
    permission_classes = [IsAdmin]


class OrganizationUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrganizationUser.objects.all()
    serializer_class = OrganizationUserSerializer
    permission_classes = [IsAdmin]
    lookup_field = "uid"
