from django.urls import path
from rest_auth.views import UserDetailsView


urlpatterns = [
    path('user/personal-data/', UserDetailsView.as_view()),
]

