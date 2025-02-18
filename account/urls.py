from django.urls import path
from . import views

urlpatterns = [
    path("register", views.RegisterView.as_view(), name="register"),
    path("login", views.LoginView.as_view(), name="login"),
    path("", views.Home.as_view(), name="home"),

    path('profile', views.UserProfileView.as_view(), name='user-profile'),

    path("user", views.UserListCreateView.as_view(), name="user-list-create"),
    path("user/<uuid:uid>", views.UserRetrieveUpdateDestroyView.as_view(), name="user-detail"),
    
    path("organizations", views.OrganizationListCreateView.as_view(), name="organization-list-create"),
    path("organizations/<uuid:uid>", views.OrganizationRetrieveUpdateDestroyView.as_view(), name="organization-detail"),


    path("organization-users", views.OrganizationUserListCreateView.as_view(), name="organization-user-list-create"),
    path("organization-users/<uuid:uid>", views.OrganizationUserRetrieveUpdateDestroyView.as_view(), name="organization-user-detail"),
]
