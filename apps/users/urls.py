from django.urls import path
from rest_auth.views import UserDetailsView

from apps.users.views import UserDataForStaffView, UserEventsViewSet

userpatterns = [
    path('me/', UserDetailsView.as_view()),
    path('<str:uuid>/', UserDataForStaffView.as_view()),
    path('me/events/', UserEventsViewSet.as_view({'get': 'list'})),
    path('me/events/<event_id>/', UserEventsViewSet.as_view({'get': 'retrieve'})),
]
