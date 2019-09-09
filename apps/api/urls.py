from django.urls import re_path, path, include
from rest_framework.routers import DefaultRouter
from rest_auth.registration.views import RegisterView
from rest_auth.views import LogoutView, LoginView
from apps.events import views as event_views


app_name = "api"

authpatterns = [
    path('registration/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]

router = DefaultRouter()
router.register(r'events', event_views.EventViewSet, basename='event')

urlpatterns = [
    path(r'auth/', include(authpatterns)),
]

urlpatterns += router.urls
