from django.urls import path
from rest_auth.views import UserDetailsView

from apps.users.views import UserDataForStaffView, OrganizationsView

userpatterns = [
    path('me/', UserDetailsView.as_view()),
    path('<str:uuid>/', UserDataForStaffView.as_view())
]

organization_patterns = [
    path('', OrganizationsView.as_view()),
]