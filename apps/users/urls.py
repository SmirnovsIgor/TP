from django.urls import path
from rest_auth.views import UserDetailsView

from apps.users.views import UserDataForStaffView

urlpatterns = [
    path('user/me/', UserDetailsView.as_view()),
    path('user/<str:uuid>', UserDataForStaffView.as_view())
]

