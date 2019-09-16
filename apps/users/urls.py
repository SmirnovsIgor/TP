from django.urls import path
from rest_auth.views import UserDetailsView


userpatterns = [
    path('me/', UserDetailsView.as_view()),
]
