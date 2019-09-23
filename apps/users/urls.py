from django.urls import path
from rest_auth.views import UserDetailsView

from apps.users.views import UserDataForStaffView, UserEventsViewSet

userpatterns = [
    path('me/', UserDetailsView.as_view()),
    path('<str:user_id>/', UserDataForStaffView.as_view()),
    path('me/events/', UserEventsViewSet.as_view({'get': 'list'})),
    path('me/events/<str:event_id>/detailed/', UserEventsViewSet.as_view({'get': 'retrieve'})),
]
