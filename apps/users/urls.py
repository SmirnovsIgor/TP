from django.urls import path
from rest_auth.views import UserDetailsView

from apps.users import views

userpatterns = [
    path('me/', UserDetailsView.as_view()),
    path('<str:user_id>/', views.UserDataForStaffView.as_view())
]

organizationpatterns = [
    path('', views.OrganizationsView.as_view()),
    path('<str:organization_id>/', views.DetailsWithAllEventsOrganizationView.as_view()),
    path('<str:organization_id>/detailed/', views.DetailedOrganizationView.as_view()),
]
