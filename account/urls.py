from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.UserListCreateView.as_view(), name='user-list-create'),
    path('user/<uuid:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('user/<uuid:pk>/delete/', views.UserDeleteView.as_view(), name='user-delete'),  

    path('organizations/', views.OrganizationListCreateView.as_view(), name='organization-list-create'),
    path('organizations/<uuid:pk>/', views.OrganizationDetailView.as_view(), name='organization-detail'),
    path('organizations/<uuid:pk>/delete/', views.OrganizationDeleteView.as_view(), name='organization-delete'),  

    path('organization-user/', views.OrganizationUserListCreateView.as_view(), name='organization-user-list-create'),
    path('organization-user/<uuid:pk>/', views.OrganizationUserDetailView.as_view(), name='organization-user-detail'),
]
