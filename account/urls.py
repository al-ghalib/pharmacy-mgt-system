from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("", views.Home.as_view(), name="home"),

    path("user/", views.UserListCreateView.as_view(), name="user-list-create"),
    path("user/<uuid:uid>/", views.UserDetailView.as_view(), name="user-detail"),
    path(
        "users/<uuid:uid>/update/", views.UserUpdateView.as_view(), name="user-update"
    ),
    path("user/<uuid:uid>/delete/", views.UserDeleteView.as_view(), name="user-delete"),
 
    path(
        "organizations/",
        views.OrganizationListCreateView.as_view(),
        name="organization-list-create",
    ),
    path(
        "organizations/<uuid:uid>/",
        views.OrganizationDetailView.as_view(),
        name="organization-detail",
    ),
    path(
        "organizations/<uuid:uid>/update/",
        views.OrganizationUpdateView.as_view(),
        name="organization-update",
    ),
    path(
        "organizations/<uuid:uid>/delete/",
        views.OrganizationDeleteView.as_view(),
        name="organization-delete",
    ),
    
    path(
        "organization-users/",
        views.OrganizationUserListCreateView.as_view(),
        name="organization-user-list-create",
    ),
    path(
        "organization-users/<uuid:uid>/",
        views.OrganizationUserDetailView.as_view(),
        name="organization-user-detail",
    ),
    # path('organization-users/<uuid:uid>/update/', views.OrganizationUserUpdateView.as_view(), name='organization-user-update'),
    # path('organization-users/<uuid:uid>/delete/', views.OrganizationUserDeleteView.as_view(), name='organization-user-delete'),
]
