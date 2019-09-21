from django.urls import path
from rest_auth.views import UserDetailsView

from apps.users.views import UserDataForStaffView, UserEventsView

userpatterns = [
    path('me/', UserDetailsView.as_view()),
    path('<str:uuid>/', UserDataForStaffView.as_view()),
    path('me/events/', UserEventsView.as_view()),
]
