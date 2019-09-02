from django.urls import path, re_path
from rest_framework.routers import DefaultRouter

from apps.events import views


app_name = "events"

router = DefaultRouter()
router.register(r'events', views.EventViewSet, basename='event')

urlpatterns = [
    path('', views.EventList.as_view(), name='events_list'),
    path('<uuid:id>/', views.EventDetail.as_view(), name='events_detail'),
]

urlpatterns += router.urls
